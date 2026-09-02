# 03 Event — ocurrencia discreta en un tick
# PRE: -
# POST: evento ON_TEST emitido y procesado
from gamestate import GameState
from effects import emit

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    emit("ON_TEST", source=hero.id)(gs, {})
