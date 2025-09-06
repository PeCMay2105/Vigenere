from collections import deque
import string


class VigenereAttack:
    def __init__(self, portuguese: bool = False):
        """Configura análise de frequência para português ou inglês."""
        self.frequency = (
            {
                'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
                'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40, 'K': 0.02,
                'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 'Q': 1.20,
                'R': 6.53, 'S': 7.81, 'T': 4.34, 'U': 4.63, 'V': 1.67, 'W': 0.01,
                'X': 0.21, 'Y': 0.01, 'Z': 0.47
            }
            if portuguese else
            {
                'A': 8.167, 'B': 1.492, 'C': 2.78, 'D': 4.253, 'E': 12.702,
                'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
                'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
                'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
                'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
                'Z': 0.074
            }
        )

    # -----------------------------
    #   MÉTODOS DE ANÁLISE ESTATÍSTICA
    # -----------------------------

    def index_of_coincidence(self, text: str) -> float:
        """Calcula o índice de coincidência (IC) de um texto."""
        n = len(text)
        if n <= 1:
            return 0.0

        freqs = {ch: text.count(ch) for ch in set(text)}
        return sum(f * (f - 1) for f in freqs.values()) / (n * (n - 1))

    def find_best_keysize_by_ic(self, encrypt: str, min_size=1, max_size=20):
        """Avalia possíveis tamanhos de chave pelo índice de coincidência médio."""
        scores = []
        for keysize in range(min_size, max_size + 1):
            groups = [''.join(encrypt[i] for i in range(j, len(encrypt), keysize))
                      for j in range(keysize)]

            avg_ic = sum(self.index_of_coincidence(g) for g in groups) / keysize
            scores.append((keysize, avg_ic))

        return sorted(scores, key=lambda x: -x[1])

    def get_top_keysizes(self, encrypt: str, top=5):
        """Retorna os tamanhos de chave mais prováveis."""
        return [k for k, _ in self.find_best_keysize_by_ic(encrypt, 1, 16)[:top]]

    # -----------------------------
    #   MÉTODOS DE ANÁLISE DE FREQUÊNCIA
    # -----------------------------

    @staticmethod
    def shift_letter(ch: str, shift: int) -> str:
        """Aplica um deslocamento (shift) a uma letra."""
        return chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))

    def estimate_key(self, encrypt: str, keysize: int):
        """Estima a chave provável para um dado tamanho."""
        blocks = [[encrypt[i] for i in range(j, len(encrypt), keysize)]
                  for j in range(keysize)]

        estimated_key = []
        for block in blocks:
            best_shift, best_score = 0, float('-inf')

            for shift in range(26):
                shifted = [self.shift_letter(ch, shift) for ch in block]
                total = len(shifted)

                if total == 0:
                    continue

                freqs = {ch: shifted.count(ch) / total for ch in set(shifted)}

                score = sum(freqs[ch] * (self.frequency.get(ch, 0) / 100)
                            for ch in freqs)

                if score > best_score:
                    best_score, best_shift = score, shift

            estimated_key.append(best_shift)

        return estimated_key

    # -----------------------------
    #   DECRIPTAÇÃO USANDO CHAVE ESTIMADA
    # -----------------------------

    def decrypt_with_key(self, encrypt: str, key_shifts):
        """Decripta texto com base em deslocamentos estimados."""
        q = deque(key_shifts)
        result = []

        for ch in encrypt:
            if ch.isalpha():
                decrypted = chr((ord(ch) - ord('A') - q[0]) % 26 + ord('A'))
                result.append(decrypted)
                q.rotate(-1)
            else:
                result.append(ch)

        return ''.join(result)

    def attack(self, encrypt: str):
        """Executa ataque: estima chave(s) e retorna possíveis textos."""
        candidates = []
        for keysize in self.get_top_keysizes(encrypt):
            print(f"🔑 Estimando chave com tamanho {keysize}...")

            key_shifts = self.estimate_key(encrypt, keysize)
            key = ''.join(chr(s + ord('A')) for s in key_shifts)

            decrypted = self.decrypt_with_key(encrypt, key_shifts)

            print(f"Chave estimada: {key}")
            print(f"Texto estimado: {decrypted}\n")

            candidates.append((key, decrypted))

        return candidates
