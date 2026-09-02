# 113 set_pos — (entity, x, y) -> — 
# Asigna posición
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_pos ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_pos", None) or getattr(_gs, "set_pos", None) or getattr(_gs.GameState, "set_pos", None) or getattr(_dt, "set_pos", None)
    assert fn is not None, "set_pos no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 5, 6)
    eff(gs, {})
    
    assert hero.position == (5,6)
