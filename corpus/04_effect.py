# 04 Effect — función que muta GameState
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
