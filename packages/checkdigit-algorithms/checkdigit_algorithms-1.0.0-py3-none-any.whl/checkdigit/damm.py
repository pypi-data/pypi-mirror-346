# Copyright (c) 2025 Luis A. Ochoa. All rights reserved.
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <LICENSE>.

class DammAlgorithm:
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
        return sequence == DammAlgorithm.__compute(subsequence)

    @staticmethod
    def generate(sequence: str) -> str:
        """
        Appends the check digit to a given digit sequence.

        :param sequence: Digit sequence.
        :return: The sequence of digits with the calculated check digit.
        """
        if not sequence.isdigit():
            raise ValueError("The sequence must be numeric.")

        return DammAlgorithm.__compute([int(char) for char in sequence])

    @staticmethod
    def __compute(sequence: list[int]) -> str:
        """
        Damm algorithm.

        :param sequence: Digit sequence.
        :return: Sequence with checkdigit.
        """
        table = [
            [ 0, 3, 1, 7, 5, 9, 8, 6, 4, 2 ],
            [ 7, 0, 9, 2, 1, 5, 4, 8, 6, 3 ],
            [ 4, 2, 0, 6, 8, 7, 1, 3, 5, 9 ],
            [ 1, 7, 5, 0, 9, 8, 3, 4, 2, 6 ],
            [ 6, 1, 2, 3, 0, 4, 5, 9, 7, 8 ],
            [ 3, 6, 7, 4, 2, 0, 9, 5, 8, 1 ],
            [ 5, 8, 6, 9, 7, 2, 0, 1, 3, 4 ],
            [ 8, 9, 4, 5, 3, 6, 2, 0, 1, 7 ],
            [ 9, 4, 3, 8, 6, 1, 7, 2, 0, 5 ],
            [ 2, 5, 8, 1, 4, 3, 6, 7, 9, 0 ]
        ]

        last_digit = 0

        row = 0

        for col in sequence:

            last_digit = table[row][col]

            row = last_digit

        return "".join(map(str, sequence + [last_digit]))
