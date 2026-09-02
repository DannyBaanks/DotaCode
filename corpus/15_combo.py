# 15_combo.py — example_8_combo
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"mana": 100, "combo_ready": True})
        enemy = gs.spawn_entity("enemy", {"hp": 100})

        # Combo: si enemy está stuneado, daño x2
        def combo_damage(gs, ctx):
            e = gs.get_entity(enemy.id)
            if e and gs.has_modifier_type(enemy.id, "STUN"):
                e.state["hp"] -= 60  # Daño amplificado
                gs.add_output("OUT_STRING", "Combo hit!")
            elif e:
                e.state["hp"] -= 30  # Daño normal
                gs.add_output("OUT_STRING", "Normal hit")
            return gs

        # Paso 1: Aplicar stun
        apply_modifier(hero.id, enemy.id, "STUN", 3,
                       gate={ActionType.MOVE, ActionType.CAST})(gs, {})

        # Paso 2: Ejecutar combo (stun activo → daño x2)
        combo_damage(gs, {})
