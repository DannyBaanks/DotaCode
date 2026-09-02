# 06 Modifier — estado temporal con duración, gate
# PRE: -
# POST: STUN 3 ticks bloquea MOVE
from gamestate import GameState
from dtypes import ActionType
from effects import apply_modifier

def setup(gs):
    hero = gs.spawn_entity("hero", {})
    enemy = gs.spawn_entity("enemy", {})
    apply_modifier(hero.id, enemy.id, "STUN", 3, gate={ActionType.MOVE})(gs, {})
