from collections import deque
import unicodedata
import string


class Vigenere:
    def __init__(self):
        self.alphabet = string.ascii_uppercase
        self.table = self._build_table()
        self.reverse_table = { (v, k): o for (o, k), v in self.table.items() }

    def _build_table(self):
        ###Constrói a tabela de Vigenère como um dicionário.
        mp = {}
        letters = list(self.alphabet)

        for row, left in enumerate(letters):
            rotated = deque(letters)
            rotated.rotate(-row)
            for right, enc in zip(letters, rotated):
                mp[(left, right)] = enc
        return mp

    def normalize_message(self, message: str) -> str:
        ###Normaliza a mensagem: remove acentos, espaços e caracteres não alfabéticos.
        message = message.upper()
        message = ''.join(c for c in unicodedata.normalize('NFD', message) if unicodedata.category(c) != 'Mn')
        return ''.join(c for c in message if c.isalpha())

    def _generate_keystream(self, text: str, keyword: str) -> str:
        ###Gera o keystream do mesmo tamanho do texto.
        keyword = self.normalize_message(keyword)
        if not keyword:
            raise ValueError("A palavra-chave não pode ser vazia.")

        q = deque(keyword)
        keystream = keyword

        while len(keystream) < len(text):
            keystream += q[0]
            q.rotate(-1)

        return keystream

    def encrypt(self, message: str, keyword: str) -> str:
        ###Encripta uma mensagem usando a cifra de Vigenère
        message = self.normalize_message(message)
        keystream = self._generate_keystream(message, keyword)
        return ''.join(self.table[(m, k)] for m, k in zip(message, keystream))

    def decrypt(self, ciphertext: str, keyword: str) -> str:
        ###Decripta um texto cifrado usando a cifra de Vigenère.
        ciphertext = self.normalize_message(ciphertext)
        keystream = self._generate_keystream(ciphertext, keyword)
        return ''.join(self.reverse_table[(c, k)] for c, k in zip(ciphertext, keystream))
