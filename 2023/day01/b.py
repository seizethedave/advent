import sys

def first_digit(s, rev):
    tr = translations
    if rev:
        s = s[::-1]
        tr = {l[::-1]: r for l, r in translations.items()}
    for i in range(len(s)):
        if s[i].isdigit():
            return s[i]
        elif s[i].isalpha():
            for l, r in tr.items():
                try:
                    match = s[i:i+len(l)] == l
                except IndexError:
                    continue
                else:
                    if match:
                        return r

translations = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def iter_calibration_values(lines):
    for line in lines:
        first = first_digit(line, False)
        last = first_digit(line, True)
        yield int(f'{first}{last}')


print(sum(iter_calibration_values(line.strip() for line in sys.stdin)))
