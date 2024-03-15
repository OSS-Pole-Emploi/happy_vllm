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

from happy_vllm import utils


class VLLMLogitsProcessorResponsePool:

    def __init__(self, tokenizer, possible_responses: List[str]) -> None:
        '''Initializes the logits processor with the token ids of the possible responses

        Args:
            tokenizer : The tokenizer used by the model
            possible_responses (list) : The list containing all the possible responses from which the llm will choose from

        '''
        self.possible_tokens_responses = {response: list(utils.proper_tokenization(tokenizer, response)) for response in possible_responses}
        self.eos_token_id = tokenizer.eos_token_id

    def __call__(self, input_ids: List[int], scores: torch.Tensor) -> torch.Tensor:
        """Puts a mask to allow only tokens which could provide a response in the pool

        Args:
            inputs_ids (list) : The list of tokens ids generated by the LLM
            scores (torch.tensor) : The tensor containing the logits for the next token
        
        Returns:
            toch.tensor : The updated scores ie the initial scores masked to only allow possible tokens

        """
        if self.possible_tokens_responses == {}:
            return scores
        # Gets the next possible tokens
        allowed_tokens = self._get_next_possible_tokens(input_ids)
        # Compute the corresponding mask
        mask = torch.full_like(scores, -math.inf)
        mask[allowed_tokens] = 0
        # Mask the scores
        scores = scores + mask
        return scores

    def _get_next_possible_tokens(self, input_ids: List[int]) -> List[int]:
        """Gets the next possible tokens for the response to be in the allowed pool

        Args:
            inputs_ids (list) : The list of tokens ids generated by the LLM
        
        Returns:
            list : The list of possible following tokens
        """
        allowed_tokens = set()
        # If we are not "in" a response (ie this is the first token generated)
        if len(input_ids) == 0:
            # We allow all first tokens of all possible responses
            allowed_tokens = {possible_responses_ids[0] for possible_responses_ids in self.possible_tokens_responses.values()}
        else:
            # For each possible responses...
            for possible_responses, possible_responses_ids in self.possible_tokens_responses.items():
                # Get the index at which the input corresponds to this response
                i_current_token = self._get_common_tokens_ids_end_begin(input_ids, possible_responses_ids)
                # If not 0, then, we are "in" this response
                if i_current_token != 0:
                    # We are at the end of the respons so -> eos token
                    if i_current_token >= len(possible_responses_ids):
                        allowed_tokens.add(self.eos_token_id)
                    # We are in the middle of the response -> give the following token in the response
                    else:
                        allowed_tokens.add(possible_responses_ids[i_current_token])
        allowed_tokens = list(allowed_tokens)
        return allowed_tokens

    def _get_common_tokens_ids_end_begin(self, list_end: list, list_begin: list) -> int:
        """Gives the index where we are with common elements at the end of list_end and at the beginning of list_begin. For
        example if list_end = [1, 2, 3, 4] and list_begin = [3, 4, 5] we return 2

        Args:
            list_end (list) : The list where we look at the end
            list_begin (list) : The list where we look at the beginning
        
        Returns:
            int : The index (or number) of common elements at the end of list_end and at the beginning of list_begin

        """
        i = len(list_begin)
        while list_begin[:i] != list_end[-i:] and i > 0:
            i -= 1
        return i