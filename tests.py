import unittest
import sphinxator


class TestCipherMethods(unittest.TestCase):

    def test_cezar(self):
        text = "percival probitas"
        encrypted = sphinxator.cezar(text, 4)
        self.assertEqual("tivgmzep tvsfmxew", encrypted)

    def test_cezar_loops(self):
        text = "percival probitas"
        encrypted = sphinxator.cezar(text, 26)
        self.assertEqual(text, encrypted)

    def test_cezar_loops2(self):
        text = "percival probitas"
        encrypted = sphinxator.cezar(text, 4)
        encrypted2 = sphinxator.cezar(text, 30)
        self.assertEqual(encrypted, encrypted2)

    def test_cezar_negative(self):
        text = "percival probitas"
        encrypted = sphinxator.cezar(text, -4)
        self.assertEqual("lanyerwh lnkxepwo", encrypted)

    def test_harcerski(self):
        text = "percival probitas"
        encrypted = sphinxator.harcerski(text, "GA-DE-RY-PO-LU-KI")
        self.assertEqual("odyckvgu oypbktgs", encrypted)

    def test_vigenere(self):
        text = "percival probitas"
        key = "consilium"
        encrypted = sphinxator.vigenere(text, key)
        self.assertEqual("rseuqgif btcoabla", encrypted)

    def test_vigenere_decrypt(self):
        text = "rseuqgif btcoabla"
        key = "consilium"
        decrypted = sphinxator.vigenere(text, key, decrypt=True)
        self.assertEqual("percival probitas", decrypted)

    def test_playfair_encrypt(self):
        text = "secret message"
        key = "keyword"
        encrypted = sphinxator.playfair(text, key)
        self.assertEqual("nordkunkqzpcnd", encrypted)

    def test_playfair_decrypt(self):
        text = "nordkunkqzpcnd"
        key = "keyword"
        decrypted = sphinxator.playfair(text, key, decrypt=True)
        self.assertEqual()