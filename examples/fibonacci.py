# Fibonacci DotaCode — 10 terminos (0 1 1 2 3 5 8 13 21 34)
# Demuestra runtime completo: Entity, State, Event, Trigger, Time
# Sin bucle Python: el motor run_loop despacha ON_FIB y aplica effects
# Cada termino se emite como OUT_NUMBER, visible en gs.output

import sys, os
try:
    _here = os.path.dirname(__file__)
except NameError:
    _here = os.path.dirname(os.path.abspath("examples/fibonacci.py"))
    # host exec no define __file__, usa ruta conocida
    _here = r"C:\Development\ISyCo Git\DotaCode\examples"
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
