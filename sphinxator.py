#!/usr/bin/env/python
"""
sphinxator - szyfrator/deszyfrator LSM

Michał Szewczak 2016
"""


def is_lowercase_letter(c):
    return ord('a') <= ord(c) <= ord('z')


def cezar(text, shift):
    text = text.lower()

    encrypted = []
    for c in text:
        if not is_lowercase_letter(c):
            new_c = c
        else:
            new_c = chr((ord(c)-ord('a')+shift)+ord('a'))
        encrypted.append(new_c)

    return "".join(encrypted)


def harcerski(text, template):
    # strip dashes
    template = "".join(template.split('-'))
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
        if not is_lowercase_letter(c):
            new_c = c
        else:
            new_c = mapping[c]
        encrypted.append(new_c)

    return "".join(encrypted)