# Fibonacci DotaCode CORE — 10 terminos (0 1 1 2 3 5 8 13 21 34)
# STATUS: DEMONSTRATED via core primitives (INC/JZDEC) — no custom Python c=a+b
# Compila una máquina de contadores a triggers con inc_state/dec_state/emit.
# Python solo ensambla; run_loop despacha y el motor decide bifurcación.
# Cada termino se emite con output_number (efecto del runtime, no Python).
# Equivalente fuerte a SpellCode/DuelCode/PokéCode.

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
from effects import dec_state, emit, inc_state, set_state
from runtime import run

def output_reg(eid, reg):
    def _eff(gs, ctx):
        e = gs.get_entity(eid)
        if e:
            gs.add_output("OUT_NUMBER", e.state.get(reg, 0))
        return gs
    return _eff

# --- Helpers para compilar Minsky con OUT ---
def _mayor_que_cero(eid, reg):
    def cond(gs, ev):
        e = gs.get_entity(eid)
        return bool(e) and e.state.get(reg, 0) > 0
    return cond

def _igual_a_cero(eid, reg):
    def cond(gs, ev):
        e = gs.get_entity(eid)
        return not e or e.state.get(reg, 0) == 0
    return cond

def compilar_fib(gs, programa, registros, inicio):
    eid = gs.spawn_entity("fib_core", dict(registros, halted=0)).id
    for estado, instr in programa.items():
        ev = f"STATE_{estado}"
        op = instr[0]
        if op == "INC":
            _, reg, nxt = instr
            gs.add_trigger(Trigger(id=gs.new_trigger_id(), on=ev, source=eid,
                then=[inc_state(eid, reg), emit(f"STATE_{nxt}", source=eid)]))
        elif op == "JZDEC":
            _, reg, a,b = instr
            gs.add_trigger(Trigger(id=gs.new_trigger_id(), on=ev, source=eid,
                if_cond=_mayor_que_cero(eid, reg),
                then=[dec_state(eid, reg), emit(f"STATE_{a}", source=eid)]))
            gs.add_trigger(Trigger(id=gs.new_trigger_id(), on=ev, source=eid,
                if_cond=_igual_a_cero(eid, reg),
                then=[emit(f"STATE_{b}", source=eid)]))
        elif op == "OUT":
            _, reg, nxt = instr
            # need eid capture; use closure via helper
            def _make_out(r, n):
                return [output_reg(eid, r), emit(f"STATE_{n}", source=eid)]
            gs.add_trigger(Trigger(id=gs.new_trigger_id(), on=ev, source=eid,
                then=_make_out(reg, nxt)))
        elif op == "HALT":
            gs.add_trigger(Trigger(id=gs.new_trigger_id(), on=ev, source=eid,
                then=[set_state(eid, "halted", 1)]))
    from dtypes import Event
    gs.events.push(Event(id=gs.new_event_id(), tick=0, type=f"STATE_{inicio}", source=eid))
    return eid

def INC(r,n): return ("INC", r, n)
def JZDEC(r,a,b): return ("JZDEC", r, a, b)
def OUT(r,n): return ("OUT", r, n)
HALT = ("HALT",)

# Programa Minsky para Fibonacci 10 términos
# Registros: a,b,n,c,tmp
# Emite a cada iteración, luego c=a+b via copias con tmp, luego a=b, b=c, n--, loop
prog = {
    "LOOP": OUT("a", "CLR_C"),
    "CLR_C": JZDEC("c", "CLR_C", "COPY_A"),
    "COPY_A": JZDEC("a", "COPY_A_CONT", "REST_A"),
    "COPY_A_CONT": INC("c", "COPY_A_CONT2"),
    "COPY_A_CONT2": INC("tmp", "COPY_A"),
    "REST_A": JZDEC("tmp", "REST_A_CONT", "COPY_B"),
    "REST_A_CONT": INC("a", "REST_A"),
    "COPY_B": JZDEC("b", "COPY_B_CONT", "REST_B"),
    "COPY_B_CONT": INC("c", "COPY_B_CONT2"),
    "COPY_B_CONT2": INC("tmp", "COPY_B"),
    "REST_B": JZDEC("tmp", "REST_B_CONT", "CLR_A"),
    "REST_B_CONT": INC("b", "REST_B"),
    "CLR_A": JZDEC("a", "CLR_A", "COPY_B_TO_A"),
    "COPY_B_TO_A": JZDEC("b", "COPY_B_TO_A_CONT", "REST_B2"),
    "COPY_B_TO_A_CONT": INC("a", "COPY_B_TO_A_CONT2"),
    "COPY_B_TO_A_CONT2": INC("tmp", "COPY_B_TO_A"),
    "REST_B2": JZDEC("tmp", "REST_B2_CONT", "CLR_B"),
    "REST_B2_CONT": INC("b", "REST_B2"),
    "CLR_B": JZDEC("b", "CLR_B", "COPY_C_TO_B"),
    "COPY_C_TO_B": JZDEC("c", "COPY_C_TO_B_CONT", "REST_C"),
    "COPY_C_TO_B_CONT": INC("b", "COPY_C_TO_B_CONT2"),
    "COPY_C_TO_B_CONT2": INC("tmp", "COPY_C_TO_B"),
    "REST_C": JZDEC("tmp", "REST_C_CONT", "DEC_N"),
    "REST_C_CONT": INC("c", "REST_C"),
    "DEC_N": JZDEC("n", "LOOP", "HALT"),
    "HALT": HALT,
}

def setup(gs):
    # n=9 da 10 emisiones con esta lógica JZDEC (ver DuelCode fibonacci)
    compilar_fib(gs, prog, {"a":0,"b":1,"n":9,"c":0,"tmp":0}, "LOOP")

if __name__ == "__main__":
    from runtime import run
    gs = run(seed=42, setup_fn=setup, max_ticks=100000)
    out = [o.value for o in gs.output if o.type=="OUT_NUMBER"]
    # También hay OUT_NUMBER de cada LOOP
    print("fib_core:", out)
    assert out == [0,1,1,2,3,5,8,13,21,34], f"got {out}"
    print("Fibonacci CORE 10 OK (solo inc_state/dec_state/emit, motor decide)")

# Para host.py
# host.py espera setup(gs) definido arriba, así que `py host.py examples/fibonacci_core.py` funciona
