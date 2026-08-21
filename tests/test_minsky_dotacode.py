"""Reduccion REAL: maquina de contadores ejecutada por el runtime de DotaCode.

A diferencia de `tests/testurings.py` -- que calcula en Python y guarda el
resultado en `gs.globals` -- aqui Python solo ensambla triggers. El computo lo
hace `run_loop` despachando eventos y aplicando efectos del motor.

El test `test_el_motor_hace_el_trabajo` es el que separa una cosa de la otra:
comprueba que sin motor no hay resultado.
"""

from __future__ import annotations

import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "src"))

from minsky_dotacode import (HALT, INC, JZDEC, compilar,   # noqa: E402
                             ejecutar, multiplica, suma)
from gamestate import GameState                            # noqa: E402


class TestMinskyReal(unittest.TestCase):

    def test_suma_dos_contadores(self):
        """Dos registros exactos: la hipotesis literal de Minsky (1967)."""
        for a, b in ((2, 3), (7, 5), (0, 4), (9, 0)):
            with self.subTest(a=a, b=b):
                estado = suma(a, b)
                self.assertEqual(estado["a"], a + b)
                self.assertEqual(estado["b"], 0)
                self.assertEqual(estado["halted"], 1)

    def test_multiplicacion(self):
        for a, b in ((3, 4), (6, 7), (0, 9), (5, 1)):
            with self.subTest(a=a, b=b):
                self.assertEqual(multiplica(a, b)["acc"], a * b)

    def test_solo_usa_dos_registros_en_la_suma(self):
        estado = suma(3, 4)
        registros = {k for k in estado if k != "halted"}
        self.assertEqual(registros, {"a", "b"})

    def test_la_bifurcacion_la_decide_el_motor(self):
        """JZDEC son dos triggers con condiciones excluyentes, no un if."""
        cero = ejecutar({"1": JZDEC("x", "2", "3"),
                         "2": INC("marca_no_cero", "3"),
                         "3": HALT}, {"x": 0}, "1")
        self.assertNotIn("marca_no_cero", cero)

        no_cero = ejecutar({"1": JZDEC("x", "2", "3"),
                            "2": INC("marca_no_cero", "3"),
                            "3": HALT}, {"x": 1}, "1")
        self.assertEqual(no_cero["marca_no_cero"], 1)
        self.assertEqual(no_cero["x"], 0)

    def test_el_motor_hace_el_trabajo(self):
        """Sin `run_loop` no hay resultado: el computo no esta en Python.

        Se compila el programa (se registran triggers y se encola el evento
        inicial) pero NO se ejecuta el bucle. Si el calculo estuviera en Python
        como en testurings.py, el resultado ya estaria hecho.
        """
        gs = GameState(seed=1)
        eid = compilar(gs, {"1": JZDEC("b", "2", "3"),
                            "2": INC("a", "1"),
                            "3": HALT},
                       {"a": 0, "b": 5}, "1")
        estado = gs.get_entity(eid).state
        self.assertEqual(estado["a"], 0)        # nada sumado todavia
        self.assertEqual(estado["b"], 5)        # nada consumido
        self.assertEqual(estado["halted"], 0)
        self.assertFalse(gs.events.is_empty())  # el trabajo esta encolado

        # y ahora, con el motor:
        from runtime import run_loop
        gs = run_loop(gs, max_ticks=20000)
        estado = gs.get_entity(eid).state
        self.assertEqual(estado["a"], 5)
        self.assertEqual(estado["halted"], 1)

    def test_los_triggers_son_del_runtime(self):
        """Los triggers registrados son objetos Trigger de DotaCode."""
        gs = GameState(seed=1)
        compilar(gs, {"1": INC("a", "2"), "2": HALT}, {"a": 0}, "1")
        self.assertGreaterEqual(len(gs.triggers), 2)
        # gs.triggers es un dict id -> Trigger
        for t in gs.triggers.values():
            self.assertTrue(t.on.startswith("STATE_"))
            self.assertTrue(t.then)


if __name__ == "__main__":
    unittest.main(verbosity=2)
