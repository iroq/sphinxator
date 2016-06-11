import unittest
from sphinxator import cezar, harcerski, vigenere


class TestCipherMethods(unittest.TestCase):

    def test_cezar(self):
        text = "percival probitas"
        encrypted = cezar(text, 4)
        self.assertEqual("tivgmzep tvsfmxew", encrypted)

    def test_cezar_loops(self):
        text = "percival probitas"
        encrypted = cezar(text, 26)
        self.assertEqual(text, encrypted)

    def test_cezar_loops2(self):
        text = "percival probitas"
        encrypted = cezar(text, 4)
        encrypted2 = cezar(text, 30)
        self.assertEqual(encrypted, encrypted2)

    def test_cezar_negative(self):
        text = "percival probitas"
        encrypted = cezar(text, -4)
        self.assertEqual("lanyerwh lnkxepwo", encrypted)

    def test_harcerski(self):
        text = "percival probitas"
        encrypted = harcerski(text, "GA-DE-RY-PO-LU-KI")
        self.assertEqual("odyckvgu oypbktgs", encrypted)

    def test_vigenere(self):
        text = "percival probitas"
        key = "consilium"
        encrypted = vigenere(text, key)
        self.assertEqual("rseuqgif btcoabla", encrypted)

    def test_vigenere_decrypt(self):
        text = "rseuqgif btcoabla"
        key = "consilium"
        decrypted = vigenere(text, key, decrypt=True)
        self.assertEqual("percival probitas", decrypted)