"""Maquina de contadores compilada a triggers de DotaCode.

POR QUE EXISTE ESTE ARCHIVO
---------------------------
`tests/testurings.py` NO es una reduccion: calcula en Python y guarda el
resultado en `gs.globals`. Su bucle interprete es un `for` de Python y sus
"instrucciones" son operaciones sobre un dict:

    if instr[0] == "INC":
        e.state[reg] = e.state.get(reg, 0) + 1      # Python, no DotaCode

Esto es lo contrario. Python solo ENSAMBLA: construye triggers y los registra.
Quien ejecuta es `run_loop` de DotaCode, despachando eventos sobre triggers y
aplicando efectos del runtime (`inc_state`, `dec_state`, `emit`). Si se quita el
motor de DotaCode, aqui no queda nada que corra.

LA TRADUCCION
-------------
Cada estado del programa es un TIPO DE EVENTO. Cada instruccion, uno o dos
triggers que lo escuchan.

    INC(r, j)        trigger ON STATE_i -> [inc_state(r), emit(STATE_j)]

    JZDEC(r, j, k)   trigger ON STATE_i  si contador > 0
                         -> [dec_state(r), emit(STATE_j)]
                     trigger ON STATE_i  si contador == 0
                         -> [emit(STATE_k)]

    HALT             trigger ON STATE_i -> [set_state("halted", 1)]

Las dos ramas de JZDEC son triggers distintos con condiciones mutuamente
excluyentes: la bifurcacion la decide el motor al evaluar `if_cond`, no un `if`
de Python.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from dtypes import Event, Trigger            # noqa: E402
from effects import dec_state, emit, inc_state, set_state   # noqa: E402
from runtime import run                      # noqa: E402


def INC(registro: str, siguiente: str):
    return ("INC", registro, siguiente)


def JZDEC(registro: str, si_no_cero: str, si_cero: str):
    return ("JZDEC", registro, si_no_cero, si_cero)


HALT = ("HALT",)


def _mayor_que_cero(eid: int, registro: str):
    def cond(gs, ev):
        e = gs.get_entity(eid)
        return bool(e) and e.state.get(registro, 0) > 0
    return cond


def _igual_a_cero(eid: int, registro: str):
    def cond(gs, ev):
        e = gs.get_entity(eid)
        return not e or e.state.get(registro, 0) == 0
    return cond


def compilar(gs, programa: dict, registros: dict, inicio: str) -> int:
    """Registra el programa como triggers. Devuelve el id de la entidad."""
    entidad = gs.spawn_entity("counter_machine", dict(registros, halted=0))
    eid = entidad.id

    for estado, instr in programa.items():
        evento = f"STATE_{estado}"
        clase = instr[0]

        if clase == "INC":
            _, registro, siguiente = instr
            gs.add_trigger(Trigger(
                id=gs.new_trigger_id(), on=evento, source=eid,
                then=[inc_state(eid, registro),
                      emit(f"STATE_{siguiente}", source=eid)]))

        elif clase == "JZDEC":
            _, registro, si_no_cero, si_cero = instr
            gs.add_trigger(Trigger(
                id=gs.new_trigger_id(), on=evento, source=eid,
                if_cond=_mayor_que_cero(eid, registro),
                then=[dec_state(eid, registro),
                      emit(f"STATE_{si_no_cero}", source=eid)]))
            gs.add_trigger(Trigger(
                id=gs.new_trigger_id(), on=evento, source=eid,
                if_cond=_igual_a_cero(eid, registro),
                then=[emit(f"STATE_{si_cero}", source=eid)]))

        elif clase == "HALT":
            gs.add_trigger(Trigger(
                id=gs.new_trigger_id(), on=evento, source=eid,
                then=[set_state(eid, "halted", 1)]))

        else:
            raise ValueError(f"instruccion desconocida: {clase}")

    gs.events.push(Event(id=gs.new_event_id(), tick=0,
                         type=f"STATE_{inicio}", source=eid))
    return eid


def ejecutar(programa: dict, registros: dict, inicio: str,
             max_ticks: int = 20000) -> dict:
    """Corre el programa en el motor de DotaCode. Devuelve el estado final."""
    caja = {}

    def setup(gs):
        caja["eid"] = compilar(gs, programa, registros, inicio)

    gs = run(seed=1, setup_fn=setup, max_ticks=max_ticks)
    entidad = gs.get_entity(caja["eid"])
    return dict(entidad.state) if entidad else {}


# ---------------------------------------------------------------------------
# programas de referencia
# ---------------------------------------------------------------------------

def suma(a: int, b: int) -> dict:
    """a + b sobre DOS contadores: la hipotesis literal de Minsky."""
    return ejecutar(
        {"1": JZDEC("b", "2", "3"),
         "2": INC("a", "1"),
         "3": HALT},
        {"a": a, "b": b}, "1")


def multiplica(a: int, b: int) -> dict:
    """a * b. Necesita un tercero para restaurar b: decrementar es destructivo."""
    return ejecutar(
        {"1": JZDEC("a", "2", "6"),
         "2": JZDEC("b", "3", "4"),
         "3": INC("acc", "3b"),
         "3b": INC("tmp", "2"),
         "4": JZDEC("tmp", "5", "1"),
         "5": INC("b", "4"),
         "6": HALT},
        {"a": a, "b": b, "acc": 0, "tmp": 0}, "1")


if __name__ == "__main__":
    print(__doc__)
    print("=" * 62)
    for x, y in ((2, 3), (7, 5), (0, 4)):
        print(f"  suma({x},{y})       -> a = {suma(x, y)['a']}")
    for x, y in ((3, 4), (6, 7), (0, 9)):
        print(f"  multiplica({x},{y}) -> acc = {multiplica(x, y)['acc']}")
