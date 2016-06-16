#!/usr/bin/env/python


from itertools import cycle
import sys
from base64 import b64decode
import string

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
    key = cycle("".join(key.lower().split()))
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


def playfair(text, key, decrypt=False):
    alphabet = string.ascii_lowercase
    table_size = 5
    pad_char = 'x'

    # sanitize texts
    text = text.lower().replace(' ', '')
    key = key.lower().replace(' ', '')

    # we treat I and J as the same letter
    alphabet = alphabet.replace('j', '')
    assert len(alphabet) == table_size**2
    text = text.replace('j', 'i')
    key = key.replace('j', 'i')

    # insert X's in between identical pairs
    new_text = []
    for i in range(0, len(text), 2):
        a = text[i]
        try:
            b = text[i+1]
            new_text += [a, pad_char, b] if a == b else [a, b]
        except IndexError:
            new_text.append(a)
            break

    # pad to even
    if len(new_text) % 2 != 0:
        new_text.append(pad_char)

    # prepare keytable
    processed = set()
    alphabet = list(alphabet)
    stripped = []
    for c in key:
        if not c.islower() or c in processed:
            continue
        stripped.append(c)
        alphabet.remove(c)
        processed.add(c)

    alphabet = stripped + alphabet
    keytable = {}
    assert len(alphabet) == table_size**2
    for i in range(table_size):
        for j in range(table_size):
            c = alphabet[table_size*i + j]
            keytable[(i, j)] = c
            keytable[c] = (i, j)

    # perform encryption/decryption
    result = []
    shift = -1 if decrypt else 1
    for i in range(0, len(new_text), 2):
        a = new_text[i]
        b = new_text[i+1]
        ax, ay = keytable[a]
        bx, by = keytable[b]
        if ax == bx:
            a = keytable[(ax, (ay+shift) % table_size)]
            b = keytable[(bx, (by+shift) % table_size)]
        elif ay == by:
            a = keytable[((ax+shift) % table_size, ay)]
            b = keytable[((bx+shift) % table_size, by)]
        else:
            a = keytable[ax, by]
            b = keytable[bx, ay]

        result.append(a)
        result.append(b)

    return ''.join(result)


def should_decrypt():
    ans = ""
    while ans not in ['s', 'd', 'q']:
        ans = input("Szyfruj czy deszyfruj? (s/d/q): ")
        if ans == 'q':
            return
        if ans in ['s', 'd']:
            return ans == 'd'


def process_text(func, lowercase_only = True):
    while True:
        text = input("Wpisz tekst: ")
        if text.lower() == 'q':
            return
        if (lowercase_only and
                any(not c.islower() and c != ' ' for c in text)):
            print("Tekst moze zawierac tylko litery i spacje")
            continue
        print(func(text))


def get_number(prompt):
    while True:
        text = input(prompt)
        if text.lower() == 'q':
            return
        try:
            return int(text)
        except ValueError:
            continue


def main():
    banner = r"""
           _     _                 _
 ___ _ __ | |__ (_)_ __ __  ____ _| |_ ___  _ __
/ __| '_ \| '_ \| | '_ \\ \/ / _` | __/ _ \| '__|
\__ \ |_) | | | | | | | |>  < (_| | || (_) | |
|___/ .__/|_| |_|_|_| |_/_/\_\__,_|\__\___/|_|
    |_|

szyfrator/deszyfrator LSM
v. 1.1.0
Michal "Bezduszny" Szewczak 2016

Wpisz Q, aby powrocic.
"""
    print(banner)

    menu = """
1 - GA-DE-RY-PO-LU-KI
2 - PO-LI-TY-KA-RE-NU
3 - cezar
4 - vigenere
6 - playfair """

    ans = ""
    while True:
        print(menu)
        ans = input("Wybierz numer szyfru: ").lower()
        if ans == 'q':
            sys.exit(0)
        elif ans == '1':
            process_text(lambda x: harcerski(x, "GA-DE-RY-PO-LU-KI"))
        elif ans == '2':
            process_text(lambda x: harcerski(x, "PO-LI-TY-KA-RE-NU"))
        elif ans == '3':
            decrypt = should_decrypt()
            if decrypt is None:
                continue
            shift = get_number("Podaj przesuniecie: ")
            if shift is None:
                continue
            if decrypt:
                shift = -shift
            process_text(lambda x: cezar(x, shift))
        elif ans == '4':
            decrypt = should_decrypt()
            if decrypt is None:
                continue
            key = input("Podaj klucz: ")
            if key == 'q':
                continue
            process_text(lambda x: vigenere(x, key, decrypt=decrypt))
        elif ans == '6':
            decrypt = should_decrypt()
            if decrypt is None:
                continue
            key = input("Podaj klucz: ")
            if key == 'q':
                continue
            if any(not c.islower() and c!=' ' for c in key):
                print("Klucz moze zawierac tylko litery i spacje")
                continue
            process_text(lambda x: playfair(x, key, decrypt=decrypt))
        if len(ans) == 1 and ord(ans[0]) == 53:
            print(b64decode(BSTRING).decode('utf-8'))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
