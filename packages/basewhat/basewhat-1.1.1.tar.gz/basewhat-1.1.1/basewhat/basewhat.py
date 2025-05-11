"""
Convert integers to and from strings in other bases.
"""


class BaseWhat(object):
    """
    Encode/decode arbitrary-base numbers (as strings).

    >>> b16 = BaseWhat(base=16)
    >>> b16.from_int(65535)
    'FFFF'
    >>> b16.to_int('DECAFBAD')
    3737844653

    >>> b32 = BaseWhat(digits="23456789ABCDEFGHJKLMNPQRSTUVWXYZ")
    >>> b32.from_int(32767)
    'ZZZ'
    >>> b32.from_int(9223372036854775808)
    'A222222222222'
    >>> b32.to_int('1900MIXALOT')
    Traceback (most recent call last):
    ...
    ValueError: Not a valid base 32 number
    >>> b32.from_int(11111)
    'CV9'
    >>> b32.from_int(-11111)
    '-CV9'
    >>> b32.from_int(0)
    '0'
    >>> b32.to_int('DECAFBAD')
    391186392331

    Converters are case-sensitive by default
    >>> b2 = BaseWhat(digits='aA')
    >>> b2.to_int('AaaAaaA')
    73

    ...but can be made case-insensitive
    >>> b5 = BaseWhat(base=16, case_sensitive=False)
    >>> b5.to_int('a') == b5.to_int('A')
    True
    """

    def __init__(self, base=None, digits=None, case_sensitive=True) -> None:
        """
        Construct an instance given either the base or an explicit set of symbols to use for digits.

        :param int base: The number base (optional, if `digits` is specified)
        :param str digits: A string containing this base's digits, in order (optional, if `base` is specified and is 36 or less)
        :param bool case_sensitive: For digit sets with alphabetic characters, make lowercase/uppercase significant (default: True)
        """
        RAW_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if not (base or digits):
            raise ValueError("Either base or digits required")
        if base and digits and base != len(digits):
            raise ValueError("Base and digits are mismatched")
        if base and base > len(RAW_DIGITS) and not digits:
            raise ValueError("Must specify digits for bases over 36")
        if base and not digits:
            self.base = base
            self.digits = RAW_DIGITS[:base]
        if digits:
            self.digits = digits
            self.base = len(digits)
        self.case_sensitive = case_sensitive

    def valid_digit(self, d: str) -> bool:
        if self.case_sensitive:
            return d in self.digits
        else:
            return d.upper() in self.digits.upper()

    def digit_value(self, digit: str) -> int:
        if self.case_sensitive:
            return self.digits.index(digit)
        else:
            return self.digits.upper().index(digit.upper())

    def from_int(self, num: int) -> str:
        result = ""
        negative = False
        if num == 0:
            result = "0"
        elif num < 0:
            num = abs(num)
            negative = True
        while num:
            digitval = num % self.base
            result = self.digits[digitval] + result
            num //= self.base
        if negative:
            result = "-" + result
        return result

    def to_int(self, encoded: str) -> int:
        if any((not self.valid_digit(d) for d in encoded)):
            raise ValueError("Not a valid base {0} number".format(self.base))
        result = 0
        for pos, digit in enumerate(encoded):
            result += self.digit_value(digit) * pow(self.base, len(encoded) - pos - 1)
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Tests complete.")
