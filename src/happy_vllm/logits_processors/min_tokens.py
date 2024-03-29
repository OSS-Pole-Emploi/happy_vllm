#!/usr/bin/env python3
# Copyright (C) <2018-2024>  <Agence Data Services, DSI France Travail>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math
import torch
from typing import List

class VLLMLogitsProcessorMinTokens:

    def __init__(self, tokenizer, min_tokens: int) -> None:
        '''Initializes the logits processor with min_tokens

        Args:
            tokenizer : The tokenizer used by the model
            min_tokens (int) : The minimal number of tokens we want to generate 

        '''
        self.min_tokens = min_tokens
        self.eos_token_id = tokenizer.eos_token_id


    def __call__(self, input_ids: List[int], scores: torch.Tensor) -> torch.Tensor:
        """Prevents the generation of the eos token before min_tokens is reached

        Args:
            inputs_ids (list) : The list of tokens ids generated by the LLM
            scores (torch.tensor) : The tensor containing the logits for the next token
        
        Returns:
            toch.tensor : The updated scores ie the initial scores masked to only allow possible tokens
        """
        if len(input_ids) < self.min_tokens:
            mask = torch.full_like(scores, 0)
            mask[self.eos_token_id] = -math.inf
            scores = scores + mask
        return scores