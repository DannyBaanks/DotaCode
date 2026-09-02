# 07 Time — tick monótono + cola ordenada
# PRE: tick=0
# POST: tick=3 tras evento futuro
from gamestate import GameState
from effects import emit_delayed

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    emit_delayed("ON_FUTURE", 3, source=hero.id)(gs, {})
