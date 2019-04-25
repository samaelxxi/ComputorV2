"""
Contains Tokenizer class, which has only tokenize method
"""

from string import whitespace
from exceptions.parsing_exceptions import UnknownToken

ONE_CHAR_TOKENS = ["+", "-", "*", "/", "%", "^", "(", ")", "=", "?", "[", "]", ",", ";"]


class Tokenizer:
    """
    Class which transforms interpreter input string to list of tokens (as strings)
    """

    def tokenize(self, string):
        """
        Args:
            string: string to be tokenized

        Returns: list of tokens as strings
        """
        tokens = []

        char_idx = 0
        while char_idx < len(string):
            char = string[char_idx]

            if char in whitespace:
                char_idx += 1
                continue
            elif char.isdigit():
                char_idx, token = self._parse_number(string, char_idx)
            elif char.isalpha():
                char_idx, token = self._parse_name(string, char_idx)
            elif string[char_idx:char_idx + 2] == "**":
                char_idx += 2
                token = "**"
            elif char in ONE_CHAR_TOKENS:
                char_idx += 1
                token = char
            else:
                raise UnknownToken(char)
            tokens.append(token)

        return tokens

    @staticmethod
    def _parse_number(string, char_idx):
        start_idx = char_idx
        while char_idx < len(string) and (string[char_idx].isdigit() or string[char_idx] == '.'):
            char_idx += 1
        return char_idx, string[start_idx:char_idx]

    @staticmethod
    def _parse_name(string, char_idx):
        start_idx = char_idx
        while char_idx < len(string) and string[char_idx].isalpha():
            char_idx += 1
        return char_idx, string[start_idx:char_idx].lower()
