# Fibonacci DotaCode — 10 terminos (0 1 1 2 3 5 8 13 21 34)
# STATUS: DEMONSTRATED via custom Effect (no compilado a primitivas core)
# Demuestra runtime real: Entity, State, Event, Trigger, Time
# run_loop sí despacha ON_FIB y Trigger llama el effect, pero la transición
# Fibonacci (c=a+b, a=b, b=c) está escrita directamente en Python dentro del Effect.
# Es un ejemplo válido de custom effect sobre el runtime (un Effect puede ser callable Python),
# pero NO es equivalente a SpellCode/DuelCode/PokéCode donde la suma se compila a
# primitivas reales (inc_state/dec_state/emit) y el motor decide la bifurcación.
# Para el equivalente fuerte a Minsky, ver minsky_dotacode.py + test_el_motor_hace_el_trabajo.
# Cada termino se emite como OUT_NUMBER, visible en gs.output

import sys, os
try:
    _here = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # host exec no define __file__; ejecutar desde el directorio examples/
    _here = os.path.abspath(".")
try:
    sys.path.insert(0, os.path.join(_here, "..", "src"))
except Exception:
    pass

from dtypes import Trigger
from effects import emit
from runtime import run

def setup(gs):
    # Memoria: Entity fib con state a,b,n
    fib = gs.spawn_entity("fib", {"a": 0, "b": 1, "n": 10})
    gs.globals["fib_out"] = []

    def fib_step(gs, ctx):
        e = gs.get_entity(fib.id)
        if not e or e.state["n"] <= 0:
            return gs
        a = e.state["a"]
        b = e.state["b"]
        gs.globals["fib_out"].append(a)
        gs.add_output("OUT_NUMBER", a)  # I/O primitiva
        c = a + b
        e.state["a"] = b
        e.state["b"] = c
        e.state["n"] -= 1
        if e.state["n"] > 0:
            emit("ON_FIB", source=fib.id)(gs, ctx)
        return gs

    t = Trigger(id=gs.new_trigger_id(), on="ON_FIB", source=fib.id, then=[fib_step])
    gs.add_trigger(t)
    emit("ON_FIB", source=fib.id)(gs, {})

if __name__ == "__main__":
    gs = run(seed=42, setup_fn=setup)
    print("fib:", gs.globals["fib_out"])
    print("output:", [o.value for o in gs.output if o.type=="OUT_NUMBER"])
    assert gs.globals["fib_out"] == [0,1,1,2,3,5,8,13,21,34]
    print("Fibonacci 10 OK")
