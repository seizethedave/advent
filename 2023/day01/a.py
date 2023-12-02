import sys

def first_digit(s):
    for c in s:
        if c.isdigit():
            return c


def iter_calibration_values(lines):
    for line in lines:
        first = first_digit(line)
        last = first_digit(line[::-1])
        yield int(f'{first}{last}')


print(sum(iter_calibration_values(line.strip() for line in sys.stdin)))
