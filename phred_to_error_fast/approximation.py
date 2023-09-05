from floating_point import Double
# For the significand there is a linear relation (y = ax + b) depending
# on the modulo of the phred.
a0 = 10693649842770 // 3
b0 = 0
a1 = 16988536004734 // 3
b1 = 2651073056457780 -a1
a2 = 13494473815191 // 3
b2 = 1179558895604856 - 2 * a2

a1_factor = a1 - a0
a2_factor = ((a0 + a1_factor * 2) - a2) // 2
b1_factor = b1 - b0
b2_factor = ((b0 + b1_factor * 2) - b2) // 2


for i in range(94):
    exp = (i + 2) // 3
    mod = i % 3
    a = a0 + mod * a1_factor - (mod & 2) * a2_factor
    b = b0 + mod * b1_factor - (mod & 2) * b2_factor
    significand = a * i + b
    d = Double(False, 1023 - exp, significand)
    computed = float(d)
    actual = 10 ** (-i / 10)
    print(f"{i:2} {computed:20.8} {actual:20.8} {computed / actual}")
