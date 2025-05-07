# patriotlib/metrics.py

from dataclasses import dataclass


@dataclass
class CryptoMetrics:
    encryption_time: float         # Tenc
    decryption_time: float         # Tdec
    key_length: int               # K (бит)
    attack_probability: float     # Pattack (0 ≤ P ≤ 1)

    max_encryption_time: float = 1.0  # нормализующие константы
    max_decryption_time: float = 1.0
    max_key_length: int = 4096        # например, RSA-4096 — максимум
    max_attack_probability: float = 1.0

    weights: tuple = (0.25, 0.25, 0.25, 0.25)  # (w1, w2, w3, w4)

    def normalized(self):
        Tenc_norm = self.encryption_time / self.max_encryption_time
        Tdec_norm = self.decryption_time / self.max_decryption_time
        K_norm = self.key_length / self.max_key_length
        Pattack_norm = 1 - (self.attack_probability / self.max_attack_probability)
        return Tenc_norm, Tdec_norm, K_norm, Pattack_norm

    def efficiency_score(self) -> float:
        Tenc_n, Tdec_n, K_n, P_n = self.normalized()
        w1, w2, w3, w4 = self.weights
        return w1 * Tenc_n + w2 * Tdec_n + w3 * K_n + w4 * P_n
