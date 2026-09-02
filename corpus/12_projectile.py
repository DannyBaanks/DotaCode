# 12_projectile.py — example_5_projectile
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        caster = gs.spawn_entity("caster", {"mana": 100}, (0, 0))
        target = gs.spawn_entity("target", {"hp": 100}, (5, 0))

        # Spawn projectile que viaja hacia target
        proj = gs.spawn_entity("projectile", {"damage": 25, "speed": 2}, (0, 0), {"projectile"})

        # Movimiento periódico del proyectil
        def move_projectile(gs, ctx):
            p = gs.get_entity(proj.id)
            t = gs.get_entity(target.id)
            if p and t and p.alive and t.alive:
                # Mover 2 unidades hacia target
                dx = t.position[0] - p.position[0]
                if abs(dx) <= p.state["speed"]:
                    # Impacto!
                    t.state["hp"] -= p.state["damage"]
                    gs.add_output("OUT_STRING", f"Hit for {p.state['damage']}")
                    gs.destroy_entity(p.id)
                else:
                    p.position = (p.position[0] + p.state["speed"], p.position[1])
            return gs

        periodic(move_projectile, every=1)(gs, {})
