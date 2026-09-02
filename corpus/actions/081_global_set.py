# 081 global_set — (name, value) -> — 
# Accesible por todas las entities
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: global_set ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "global_set", None) or getattr(_gs, "global_set", None) or getattr(_gs.GameState, "global_set", None) or getattr(_dt, "global_set", None)
    assert fn is not None, "global_set no encontrado"
    # Llamada canónica real
    eff = fn('gtest', 123)
    eff(gs, {})
    
    assert gs.globals.get('gtest') == 123
