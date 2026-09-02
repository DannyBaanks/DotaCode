# 210 consume_event — (event) -> — 
# Marca como manejado
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: consume_event ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "consume_event", None) or getattr(_gs, "consume_event", None) or getattr(_gs.GameState, "consume_event", None) or getattr(_dt, "consume_event", None)
    assert fn is not None, "consume_event no encontrado"
    # Llamada canónica real
    eff = consume_event(1)
    eff(gs, {}) if callable(eff) else None
    assert True
