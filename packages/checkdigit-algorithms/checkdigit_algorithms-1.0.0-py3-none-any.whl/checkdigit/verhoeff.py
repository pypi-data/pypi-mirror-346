# Copyright (c) 2025 Luis A. Ochoa. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <LICENSE>.

class VerhoeffAlgorithm:
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
        return sequence == VerhoeffAlgorithm.__compute(subsequence)

    @staticmethod
    def generate(sequence: str) -> str:
        """
        Appends the check digit to a given digit sequence.

        :param sequence: Digit sequence.
        :return: The sequence of digits with the calculated check digit.
        """
        return VerhoeffAlgorithm.__compute([int(char) for char in sequence])

    @staticmethod
    def __compute(sequence: list[int]) -> str:
        """
        Verhoeff algorithm.

        :param sequence: Digit sequence.
        :return: Sequence with checkdigit.
        """
        inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]

        new_sequence = sequence[:]

        new_sequence.append(0)

        new_sequence.reverse()

        last_digit = inv[VerhoeffAlgorithm.__get_last_digit(new_sequence)]

        return "".join(map(str, sequence + [last_digit]))

    @staticmethod
    def __get_last_digit(sequence: list[int]):
        p = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
             [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
             [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
             [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
             [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
             [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
             [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]

        d = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
             [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
             [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
             [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
             [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
             [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
             [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
             [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
             [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
             [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]

        c = 0

        for idx, digit in enumerate(sequence):
            c = d[c][p[idx % 8][sequence[idx]]]

        return c
