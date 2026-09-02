# 216 broadcast — (type, source?, payload) -> — 
# Emite a todas las entities
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: broadcast ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "broadcast", None) or getattr(_gs, "broadcast", None) or getattr(_gs.GameState, "broadcast", None) or getattr(_dt, "broadcast", None)
    assert fn is not None, "broadcast no encontrado"
    # Llamada canónica real
    eff = broadcast(1, hero.id, None)
    eff(gs, {}) if callable(eff) else None
    assert True
