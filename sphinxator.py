#!/usr/bin/env/python
"""
sphinxator - szyfrator/deszyfrator LSM

Michał Szewczak 2016
"""
from itertools import cycle

BSTRING = (b'Ci0gQ3p5bSByb3puaSBzaWUgaW5mb3JtYXR5ayBvZCBmZW1pbmlzd'
           b'GtpPwotIEluZm9ybWF0eWsgY3phc2VtIHNpZSBkbyBjemVnb3MgcHJ6eWRhamUuCg==')


def is_lowercase_letter(c):
    return ord('a') <= ord(c) <= ord('z')


def cezar(text, shift):
    text = text.lower()

    encrypted = []
    for c in text:
        if not is_lowercase_letter(c):
            new_c = c
        else:
            new_c = chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        encrypted.append(new_c)

    return "".join(encrypted)


def harcerski(text, template):
    # strip dashes
    template = "".join(template.lower().split('-'))
    template = list(template)

    mapping = {}
    while template:
        try:
            first = template.pop()
            second = template.pop()
        except IndexError:
            print("Nieprawidlowy wzor szyfru harcerskiego (nieparzysta dlugosc)")
            return ""
        mapping[first] = second
        mapping[second] = first

    encrypted = []
    for c in text:
        if not is_lowercase_letter(c) or c not in mapping:
            new_c = c
        else:
            new_c = mapping[c]
        encrypted.append(new_c)

    return "".join(encrypted)


def vigenere(text, key, decrypt=False):
    data = []
    key = cycle(key.lower())
    for c in text.lower():
        if not is_lowercase_letter(c):
            pair = (c, 0)
        else:
            kc = next(key)
            shift = ord(kc) - ord('a')
            if decrypt:
                shift = -shift
            pair = (c, shift)

        data.append(pair)

    encrypted = []
    for (c, shift) in data:
        encrypted.append(cezar(c, shift) if shift != 0 else c)

    return "".join(encrypted)