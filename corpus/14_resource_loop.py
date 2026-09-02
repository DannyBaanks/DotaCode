# 14_resource_loop.py — example_7_resource_loop
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"mana": 20, "mana_max": 100, "mana_regen": 10})
        # El evento futuro hace transcurrir diez ticks de regeneración.
        emit_delayed("ON_TICK", 10, source=hero.id)(gs, {})
