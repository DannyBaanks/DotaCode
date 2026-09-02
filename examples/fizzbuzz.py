# FizzBuzz DotaCode 1..15 — vía custom Effect (honesto, como fibonacci.py)
# Cada iteración hace r3=i%3 y r5=i%5 en Python, pero el bucle y la salida usan Trigger/Time
# Para el equivalente fuerte a primitivas core, ver futuro fizzbuzz_core.py

import sys, os
try:
    _here = os.path.dirname(__file__)
except NameError:
    _here = r"C:\Development\ISyCo Git\DotaCode\examples"
try:
    sys.path.insert(0, os.path.join(_here, "..", "src"))
except Exception:
    pass

from dtypes import Trigger
from effects import emit
from runtime import run

def setup(gs):
    fib = gs.spawn_entity("fizz", {"i": 1, "n": 15})
    gs.globals["fizz_out"] = []
    def step(gs, ctx):
        e = gs.get_entity(fib.id)
        i = e.state["i"]
        n = e.state["n"]
        if n <= 0:
            return gs
        r3 = i % 3
        r5 = i % 5
        if r3 == 0 and r5 == 0:
            s = "FizzBuzz"
        elif r3 == 0:
            s = "Fizz"
        elif r5 == 0:
            s = "Buzz"
        else:
            s = str(i)
        gs.globals["fizz_out"].append(s)
        gs.add_output("OUT_STRING", s)
        e.state["i"] += 1
        e.state["n"] -= 1
        if e.state["n"] > 0:
            emit("ON_FIZZ", source=fib.id)(gs, ctx)
        return gs
    t = Trigger(id=gs.new_trigger_id(), on="ON_FIZZ", source=fib.id, then=[step])
    gs.add_trigger(t)
    emit("ON_FIZZ", source=fib.id)(gs, {})

if __name__ == "__main__":
    gs = run(seed=42, setup_fn=setup)
    out = [o.value for o in gs.output if o.type=="OUT_STRING"]
    print("\n".join(out))
    assert out == ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
    print("FizzBuzz 15 OK")
