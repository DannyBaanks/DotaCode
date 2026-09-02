# 124 teleport — (entity, x, y) -> — 
# Instantáneo sin trayectoria
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: teleport ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "teleport", None) or getattr(_gs, "teleport", None) or getattr(_gs.GameState, "teleport", None) or getattr(_dt, "teleport", None)
    assert fn is not None, "teleport no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 9, 9)
    eff(gs, {})
    
    assert hero.position == (9,9)
