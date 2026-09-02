# 13_aoe.py — example_6_aoe
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        caster = gs.spawn_entity("caster", {"mana": 100}, (0, 0))

        # Spawn múltiples targets
        t1 = gs.spawn_entity("target", {"hp": 100}, (2, 0), {"target"})
        t2 = gs.spawn_entity("target", {"hp": 100}, (3, 1), {"target"})
        t3 = gs.spawn_entity("target", {"hp": 100}, (10, 10), {"target"})  # fuera de rango

        # AoE: dañar a todos en radio 5 desde caster
        def aoe_damage(gs, ctx):
            center = gs.get_entity(caster.id).position
            for e in gs.alive_entities():
                if e.has_tag("target"):
                    dist = abs(e.position[0] - center[0]) + abs(e.position[1] - center[1])
                    if dist <= 5:
                        e.state["hp"] -= 30
            return gs

        aoe_damage(gs, {})
