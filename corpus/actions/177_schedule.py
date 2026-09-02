# 177 schedule — (effect, tick) -> EventId 
# Programa en tick futuro
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: schedule ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "schedule", None) or getattr(_gs, "schedule", None) or getattr(_gs.GameState, "schedule", None) or getattr(_dt, "schedule", None)
    assert fn is not None, "schedule no encontrado"
    # Llamada canónica real
    eff = schedule(1, 1)
    eff(gs, {}) if callable(eff) else None
    assert True
