# 01 Entity — entidad con identidad, estado, tags
# PRE: -
# POST: hero existe, alive=True, state hp=100
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100}, (0, 0), {"hero"})
