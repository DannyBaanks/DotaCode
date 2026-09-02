# 001 spawn_entity — (type, state, position?, tags) -> EntityId 
# Crea entity con identidad única
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: spawn_entity ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "spawn_entity", None) or getattr(_gs, "spawn_entity", None) or getattr(_gs.GameState, "spawn_entity", None) or getattr(_dt, "spawn_entity", None)
    assert fn is not None, "spawn_entity no encontrado"
    # Llamada canónica real
    dummy = gs.spawn_entity('dummy', {'hp': 10})  # segunda entity para demostrar
    assert dummy.id != hero.id
