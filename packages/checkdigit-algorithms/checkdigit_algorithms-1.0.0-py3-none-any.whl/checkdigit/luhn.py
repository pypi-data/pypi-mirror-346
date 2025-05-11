# Copyright (c) 2025 Luis A. Ochoa. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <LICENSE>.

class LuhnAlgorithm:
    def __new__(cls, *args, **kwargs):
        raise TypeError("Instance is nos allowed")

    @staticmethod
    def is_valid(sequence: str) -> bool:
        """
        Verifies whether a digit sequence is valid.

        :param sequence: Digit sequence.
        :return: true if the check digit is correct; false otherwise.
        """
        if not sequence.isdigit() or len(sequence) < 2:
            return False

        subsequence = [int(char) for char in sequence[:-1]]
        return sequence == LuhnAlgorithm.__compute(subsequence)

    @staticmethod
    def generate(sequence: str) -> str:
        """
        Appends the check digit to a given digit sequence.

        :param sequence: Digit sequence.
        :return: The sequence of digits with the calculated check digit.
        """
        if not sequence.isdigit():
            raise ValueError(f"[{sequence}] is not a digit sequence.")

        return LuhnAlgorithm.__compute([int(char) for char in sequence])

    @staticmethod
    def __compute(sequence: list[int]) -> str:
        """
        Luhn algorithm.

        :param sequence: Digit sequence.
        :return: Sequence with checkdigit.
        """
        substitute = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

        new_sequence = sequence[:]

        for idx in range(len(sequence) - 1, -1, -2):
            new_sequence[idx] = substitute[sequence[idx]]

        summation = sum(new_sequence)

        last_digit = (summation * 9) % 10

        return "".join(map(str, sequence + [last_digit]))
