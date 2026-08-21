"""PRNG determinista para DotaCode.

Implementa un generador de números aleatorios sembrado y reproducible.
Basado en xorshift64 — simple, rápido, determinista.

Referencia: SPEC §10 (determinismo)
"""


class PRNG:
    """Generador de números aleatorios determinista.

    Uso:
        rng = PRNG(seed=42)
        v1 = rng.next_int(0, 100)   # entero en [0, 100]
        v2 = rng.next_float()        # float en [0.0, 1.0)
        v3 = rng.chance(0.3)         # True con probabilidad 30%
    """

    def __init__(self, seed: int):
        self._state = seed & 0xFFFFFFFFFFFFFFFF
        if self._state == 0:
            self._state = 1

    def _step(self) -> int:
        """Un paso del xorshift64."""
        x = self._state
        x ^= (x << 13) & 0xFFFFFFFFFFFFFFFF
        x ^= (x >> 7) & 0xFFFFFFFFFFFFFFFF
        x ^= (x << 17) & 0xFFFFFFFFFFFFFFFF
        self._state = x & 0xFFFFFFFFFFFFFFFF
        return self._state

    def next_int(self, lo: int, hi: int) -> int:
        """Entero en [lo, hi] inclusive."""
        if lo >= hi:
            return lo
        span = hi - lo + 1
        return lo + (self._step() % span)

    def next_float(self) -> float:
        """Float en [0.0, 1.0)."""
        return (self._step() & 0xFFFFFFFF) / 0x100000000

    def chance(self, pct: float) -> bool:
        """True con probabilidad pct (0.0 a 1.0)."""
        return self.next_float() < pct

    def choice(self, seq):
        """Elemento aleatorio de una secuencia."""
        if not seq:
            return None
        idx = self.next_int(0, len(seq) - 1)
        return seq[idx]

    def shuffle(self, lst: list) -> list:
        """Fisher-Yates shuffle in-place, retorna la lista."""
        for i in range(len(lst) - 1, 0, -1):
            j = self.next_int(0, i)
            lst[i], lst[j] = lst[j], lst[i]
        return lst

    def checkpoint(self) -> int:
        """Guarda estado del RNG."""
        return self._state

    def restore(self, checkpoint: int):
        """Restaura estado del RNG."""
        self._state = checkpoint

    def fork(self) -> "PRNG":
        """Crea sub-RNG derivado."""
        return PRNG(self._step())
