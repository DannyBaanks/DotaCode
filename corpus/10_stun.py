# 10_stun.py — example_3_stun
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"mana": 100})
        enemy = gs.spawn_entity("enemy", {"hp": 100})

        # Aplicar STUN al enemy por 3 ticks
        apply_modifier(
            hero.id, enemy.id, "STUN", 3,
            gate={ActionType.MOVE, ActionType.CAST},
        )(gs, {})

        # Intentar castear durante stun
        gs.add_output("OUT_STRING", "attempt1")
