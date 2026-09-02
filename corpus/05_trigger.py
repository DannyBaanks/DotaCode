# 05 Trigger — vínculo evento->condición->[effects]
# PRE: -
# POST: trigger ON_TEST incrementa counter al recibir evento
from gamestate import GameState
from dtypes import Trigger
from effects import inc_state, emit

def setup(gs):
    hero = gs.spawn_entity("hero", {"counter": 0})
    gs.add_trigger(Trigger(id=gs.new_trigger_id(), on="ON_TEST", source=hero.id, then=[inc_state(hero.id, "counter")]))
    emit("ON_TEST", source=hero.id)(gs, {})
