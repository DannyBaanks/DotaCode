#!/usr/bin/env python3
"""
Genera 17 .py canónicos para DotaCode — 7 primitivas + 10 megacompose —
verificados con el runtime. Cada archivo es flashcard ejecutable.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "corpus"
OUT.mkdir(exist_ok=True)

# 7 primitivas — cada una demuestra su primitiva con forma mínima
PRIMITIVES = {
    "01_entity.py": '''# 01 Entity — entidad con identidad, estado, tags
# PRE: -
# POST: hero existe, alive=True, state hp=100
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100}, (0, 0), {"hero"})
''',
    "02_state.py": '''# 02 State — mapa clave->valor mutable por entidad
# PRE: hero hp=50
# POST: hero hp=70 (gain respeta max)
from gamestate import GameState
from effects import gain

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 50, "hp_max": 100})
    gain(hero.id, "hp", 20)(gs, {})
''',
    "03_event.py": '''# 03 Event — ocurrencia discreta en un tick
# PRE: -
# POST: evento ON_TEST emitido y procesado
from gamestate import GameState
from effects import emit

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    emit("ON_TEST", source=hero.id)(gs, {})
''',
    "04_effect.py": '''# 04 Effect — función que muta GameState
# PRE: hero hp=100
# POST: hero hp=70 (damage 30)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100})
    def damage(gs, ctx):
        e = gs.get_entity(ctx["target"])
        if e:
            e.state["hp"] -= 30
        return gs
    damage(gs, {"target": hero.id})
''',
    "05_trigger.py": '''# 05 Trigger — vínculo evento->condición->[effects]
# PRE: -
# POST: trigger ON_TEST incrementa counter al recibir evento
from gamestate import GameState
from dtypes import Trigger
from effects import inc_state, emit

def setup(gs):
    hero = gs.spawn_entity("hero", {"counter": 0})
    gs.add_trigger(Trigger(id=gs.new_trigger_id(), on="ON_TEST", source=hero.id, then=[inc_state(hero.id, "counter")]))
    emit("ON_TEST", source=hero.id)(gs, {})
''',
    "06_modifier.py": '''# 06 Modifier — estado temporal con duración, gate
# PRE: -
# POST: STUN 3 ticks bloquea MOVE
from gamestate import GameState
from dtypes import ActionType
from effects import apply_modifier

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    enemy = gs.spawn_entity("enemy", {})
    apply_modifier(hero.id, enemy.id, "STUN", 3, gate={ActionType.MOVE})(gs, {})
''',
    "07_time.py": '''# 07 Time — tick monótono + cola ordenada
# PRE: tick=0
# POST: tick=3 tras evento futuro
from gamestate import GameState
from effects import emit_delayed

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    emit_delayed("ON_FUTURE", 3, source=hero.id)(gs, {})
''',
}

# 10 megacompose — extraídos de examples_10.py, cada uno como setup independiente
# Tomamos los ejemplos ya verificados y los aislamos
import importlib.util, pathlib

SRC_EXAMPLES = ROOT / "examples" / "examples_10.py"

def extract_examples():
    text = SRC_EXAMPLES.read_text(encoding="utf-8")
    # Cada def example_N_... : extrae hasta siguiente def example_
    import re
    parts = re.split(r'\ndef (example_\d+_\w+)\(\):', text)
    # parts[0] es header, luego [name, body, name, body...]
    examples = {}
    for i in range(1, len(parts), 2):
        name = parts[i]
        body = parts[i+1]
        # body termina en siguiente def o en "# Run all"
        body = body.split("\ndef ")[0]
        # Reconstruye función completa
        func = f"def setup(gs):\n" + "\n".join("    " + line if line.strip() else "" for line in body.splitlines() if "def setup" not in line and "example_" not in line[:10])
        # Limpieza: quita prints y asserts de validación, deja solo setup interno
        # En realidad, el body de example_ contiene def setup interno y gs = run...
        # Necesitamos extraer el def setup interno
        import re as re2
        m = re2.search(r'def setup\(gs\):(.*?)(?=\n    gs = run)', body, flags=re2.S)
        if m:
            inner = m.group(1)
            func = "def setup(gs):\n" + inner
            # añade imports necesarios al header
            header = "from gamestate import GameState\nfrom dtypes import Trigger, ActionType\nfrom effects import *\nfrom triggers import *\n"
            examples[name] = header + func
    return examples

def main():
    # 7 primitivas
    for fname, src in sorted(PRIMITIVES.items()):
        (OUT / fname).write_text(src, encoding="utf-8")

    # 10 megacompose
    examples = extract_examples()
    mapping = {
        "example_1_kill_counter": "08_kill_counter.py",
        "example_2_cooldown": "09_cooldown.py",
        "example_3_stun": "10_stun.py",
        "example_4_buff": "11_buff.py",
        "example_5_projectile": "12_projectile.py",
        "example_6_aoe": "13_aoe.py",
        "example_7_resource_loop": "14_resource_loop.py",
        "example_8_combo": "15_combo.py",
        "example_9_item_ability": "16_item.py",
        "example_10_simulation": "17_simulation.py",
    }
    for ex_name, fname in mapping.items():
        if ex_name in examples:
            (OUT / fname).write_text(f"# {fname} — {ex_name}\n" + examples[ex_name], encoding="utf-8")
        else:
            print(f"warn: {ex_name} no encontrado")

    # Verificación: cada archivo debe cargar y runear sin excepción
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from runtime import run
    from gamestate import GameState

    fails = []
    for p in sorted(OUT.glob("*.py")):
        code = p.read_text(encoding="utf-8")
        ns = {}
        try:
            exec(compile(code, str(p), "exec"), ns)
            setup = ns.get("setup")
            if setup is None:
                fails.append((p.name, "sin setup"))
                continue
            gs = GameState(seed=42)
            setup(gs)
            from runtime import run_loop
            gs = run_loop(gs, max_ticks=50)
        except Exception as e:
            fails.append((p.name, str(e)[:120]))

    print(f"Generados {len(list(OUT.glob('*.py')))} .py en {OUT}/")
    if fails:
        print("FALLOS:")
        for f, e in fails:
            print(f"  {f}: {e}")
        sys.exit(1)
    print("Todos los 17 verificados.")

    # host check
    import subprocess
    for sample in ["01_entity.py", "08_kill_counter.py", "11_buff.py"]:
        r = subprocess.run([sys.executable, "host.py", str(OUT / sample)], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"host falló {sample}: {r.stderr[:200]}")
            sys.exit(1)
    print("host verifica 3 muestras OK")

if __name__ == "__main__":
    main()
