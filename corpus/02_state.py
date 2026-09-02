# 02 State — mapa clave->valor mutable por entidad
# PRE: hero hp=50
# POST: hero hp=70 (gain respeta max)
from gamestate import GameState
from effects import gain

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 50, "hp_max": 100})
    gain(hero.id, "hp", 20)(gs, {})
