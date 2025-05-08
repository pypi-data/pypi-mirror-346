# Copyright 2025 Ivan Danylenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script for extending encoder context. CLI is enabled.

Example:
>>> python3 context_extension/spline_interpolation.py --model_name_or_path="intfloat/e5-large-v2" --max_seq_length 1024 --offset=0 --output_dir="idanylenko/e5-large-v2-ctx1024"
>>> python3 context_extension/spline_interpolation.py --model_name_or_path="FacebookAI/roberta-base" --max_seq_length 1024 --offset=2 --output_dir="idanylenko/roberta-base-ctx1024"
"""

from typing import Literal
from tempfile import TemporaryDirectory
import argparse
import logging
import json

import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
from scipy.interpolate import interp1d
import numpy as np


def interpolate_embeddings(
    model_name_or_path: str,
    max_seq_length: int,
    embeddings_attr_name: str = 'embeddings.position_embeddings',
    offset: int = 0,
    interpolation_type: Literal['linear', 'quadratic', 'cubic'] = 'cubic',
    output_dir: str | None = None,
    model_kwargs: dict = {},
    verbose: bool = True,
) -> SentenceTransformer:
    """
    Extends the positional embedding space of a transformer model using
    given interpolation type. The function replaces the original
    positional embeddings with a new set of interpolated embeddings
    to support longer input sequences without additional training.

    Parameters
    ----------
    model_name_or_path : str
        Path to the SentenceTransformer model or Hugging Face model name
        to which the interpolation will be applied.
    max_seq_length : int
        The target maximum sequence length for the interpolated model
        (excluding the offset). The resulting model will support sequences
        of length `max_seq_length`, not counting special embeddings retained
        via `offset`.
    embeddings_attr_name : str, optional
        Path to the transformer model attribute with positional embeddings
        weights. Default is "embeddings.position_embeddings".
    offset : int, optional
        Number of initial embeddings to preserve without interpolation.
        For example, in RoBERTa, the first 2 embeddings correspond to
        non-positional tokens like `<s>` and `<pad>`. These
        are preserved as-is. Default is 0.
    interpolation_type : Literal['linear', 'quadratic', 'cubic'], optional
        Type of interpolation to apply. Default is 'cubic'.
    output_dir : str | None, optional
        Output directory where the modified model has to be saved. If set
        to None, model will not be saved. Default is None.
    model_kwargs : dict, optional
        Additional keyword arguments passed to the SentenceTransformer
        constructor.
    verbose : bool, optional
        Whether the function should log to console. Default is True.

    Returns
    -------
    SentenceTransformer
        A SentenceTransformer instance with extended context.
    """
    logger = logging.getLogger(__name__)
    if verbose:
        logging.basicConfig(level=logging.INFO)

    # load model
    device = model_kwargs.pop('device', 'cpu')
    sentence_transformer = SentenceTransformer(model_name_or_path, device=device, **model_kwargs)
    model = sentence_transformer._first_module().auto_model

    # get positional embeddings weight
    embeddings = model
    for attr_name in embeddings_attr_name.split('.'):
        embeddings = getattr(embeddings, attr_name)
    weight = np.array(embeddings.weight.clone().detach().tolist())

    nembs = weight.shape[0]
    ndims = weight.shape[1]

    if verbose:
        logger.info(f'Loaded model from:       {model_name_or_path}')
        logger.info(f'Original max_seq_length: {nembs}')
        logger.info(f'Target max_seq_length:   {max_seq_length}')
        logger.info(f'Offset:                  {offset}')
        logger.info(f'Interpolation type:      {interpolation_type}')
        logger.info(f'Embedding dimension:     {ndims}')

    # interpolate embeddings
    stretched_weight = np.empty((max_seq_length + offset, ndims))
    stretched_weight[:offset] = weight[:offset]
    for dim in range(ndims):
        y = weight[offset:, dim]
        spline = interp1d(np.arange(len(y)), y, kind=interpolation_type)

        x = np.linspace(0, len(y) - 1, max_seq_length)
        stretched_weight[offset:, dim] = spline(x)

    # initialize new embeddings
    embeddings = nn.Embedding(
        max_seq_length + offset, ndims,
        padding_idx=embeddings.padding_idx
    )
    embeddings.weight.data = torch.Tensor(stretched_weight)

    # set new embeddings
    *holder_attrs, target_attr_name = embeddings_attr_name.split('.')
    embeddings_holder = model
    for attr_name in holder_attrs:
        # get to the object that holds embeddings
        embeddings_holder = getattr(embeddings_holder, attr_name)
    setattr(embeddings_holder, target_attr_name, embeddings)

    # update model with regard to new embeddings
    embeddings_holder.register_buffer(
        'token_type_ids',
        torch.zeros(
            (model.config.type_vocab_size, max_seq_length + offset),
            dtype=torch.long
        )
    )
    model.config.max_position_embeddings = max_seq_length + offset
    sentence_transformer._first_module().tokenizer.model_max_length = max_seq_length
    sentence_transformer.max_seq_length = max_seq_length

    # save the model if necessary
    if output_dir is not None:
        sentence_transformer.save(output_dir)
        if verbose:
            logger.info(f'Model saved to:          {output_dir}')

        return SentenceTransformer(output_dir, device=device, **model_kwargs)

    # save to temporary directory and return newly loaded model
    with TemporaryDirectory() as temp_dir:
        sentence_transformer.save(temp_dir)
        sentence_transformer = SentenceTransformer(temp_dir, device=device, **model_kwargs)

    return sentence_transformer


def main():
    parser = argparse.ArgumentParser(description='Positional embeddings interpolation.')
    parser.add_argument(
        '--model_name_or_path', type=str, required=True,
        help=(
            'Path to the SentenceTransformer model or Hugging Face model name '
            'to which the interpolation will be applied.'
        )
    )
    parser.add_argument(
        '--max_seq_length', type=int, required=True,
        help=(
            'The target maximum sequence length for the interpolated model '
            '(excluding the offset). The resulting model will support sequences '
            'of length `max_seq_length`, not counting special embeddings retained '
            'via `offset`.'
        )
    )
    parser.add_argument(
        '--output_dir', type=str, required=True,
        help=(
            'Output directory where the modified model has to be saved. If set '
            'to None, model will not be saved. Default is None.'
        )
    )
    parser.add_argument(
        '--embeddings_attr_name', type=str, default='embeddings.position_embeddings',
        help=(
            'Path to the transformer model attribute with positional embeddings '
            'weights. Default is "embeddings.position_embeddings".'
        )
    )
    parser.add_argument(
        '--offset', type=int, default=0,
        help=(
            'Number of initial embeddings to preserve without interpolation. '
            'For example, in RoBERTa, the first 2 embeddings correspond to '
            'non-positional tokens like `<s>` and `<pad>`. These '
            'are preserved as-is. Default is 0.'
        )
    )
    parser.add_argument(
        '--interpolation_type', type=str, default='cubic',
        help='Type of interpolation. Must be one of: linear, quadratic, cubic.'
    )
    parser.add_argument(
        '--model_kwargs', type=str, default='{}',
        help='Additional keyword arguments for the model in JSON format. Default is "{}".'
    )
    parser.add_argument('--quiet', action='store_true', help='Suppress console logs.')
    args = parser.parse_args()

    # parse model_kwargs from JSON string
    model_kwargs = json.loads(args.model_kwargs)

    interpolate_embeddings(
        model_name_or_path=args.model_name_or_path,
        max_seq_length=args.max_seq_length,
        embeddings_attr_name=args.embeddings_attr_name,
        offset=args.offset,
        interpolation_type=args.interpolation_type,
        output_dir=args.output_dir,
        model_kwargs=model_kwargs,
        verbose=not args.quiet,
    )


if __name__ == '__main__':
    main()
