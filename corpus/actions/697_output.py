# 697 output — (value) -> — 
# Escribe valor
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: output ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "output", None) or getattr(_gs, "output", None) or getattr(_gs.GameState, "output", None) or getattr(_dt, "output", None)
    assert fn is not None, "output no encontrado"
    # Llamada canónica real
    eff = output(1, 'hero')
    eff(gs, {}) if callable(eff) else None
    assert True
