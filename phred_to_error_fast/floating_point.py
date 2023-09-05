import struct

SIGN_SHIFT = 63
SIGN_MASK = 1 << SIGN_SHIFT
EXPONENT_SHIFT = 52
EXPONENT_MASK = 0b111_1111_1111 << EXPONENT_SHIFT
SIGNIFICAND_MASK = (1 << EXPONENT_SHIFT) - 1


def cast_float_to_int(f: float):
    float_bytes = struct.pack("d", f)
    i, = struct.unpack("Q", float_bytes)
    return i


def cast_int_to_float(i: int):
    int_bytes = struct.pack("Q", i)
    f, = struct.unpack("d", int_bytes)
    return f


class Double:
    sign: bool
    exponent: int
    significand: int

    def __init__(self, sign, exponent: int, significand: int):
        self.sign = bool(sign)
        self.exponent = exponent
        self.significand = significand

    def significand_fraction(self):
        sig_bits = self.significand
        accumulator = 1.0
        for i in range(52, 0 , -1):
            bit = sig_bits & 1
            sig_bits >>= 1
            accumulator += bit * 2 ** -i
        return accumulator

    @classmethod
    def from_int(cls, i: int):
        return cls(
            sign=i & SIGN_MASK,
            exponent=(i & EXPONENT_MASK) >> EXPONENT_SHIFT,
            significand=i & SIGNIFICAND_MASK)

    @classmethod
    def from_float(cls, f: float):
        return cls.from_int(cast_float_to_int(f))

    def __int__(self):
        return (self.significand |
                (self.exponent << EXPONENT_SHIFT) |
                (self.sign << SIGN_SHIFT))

    def __float__(self):
        return cast_int_to_float(int(self))

    def __repr__(self):
        return (f"Double(sign={self.sign}, "
                f"exponent={self.exponent}, "
                f"significand={self.significand})")


if __name__ == "__main__":
    errors = [10 ** (i / -10) for i in range(94)]
    doubles = [Double.from_float(e) for e in errors]
    for remainder in (0, 1, 2):
        previous_significand = 0
        previous_difference = 0
        for i, d in enumerate(doubles):
            if i%3!=remainder:
                continue
            significand = d.significand
            difference = significand - previous_significand
            previous_significand = significand
            higher_order_difference = difference - previous_difference
            previous_difference = difference
            print(f"{i:2}\t{d.exponent:6}\t{d.significand:20}\t{difference:20}\t{higher_order_difference:20}\t{bin(int(d))}")

    for i in range(94):
        x = i // 3
        mod = i - (x * 3)
        d = Double(False, 1023 - x, 3564549947590 * i)
        print(i, float(d), 10 ** (-i / 10))