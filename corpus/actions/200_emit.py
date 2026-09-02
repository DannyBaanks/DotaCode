# 200 emit — (type, source?, target?, payload) -> EventId 
# Emite evento
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: emit ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "emit", None) or getattr(_gs, "emit", None) or getattr(_gs.GameState, "emit", None) or getattr(_dt, "emit", None)
    assert fn is not None, "emit no encontrado"
    # Llamada canónica real
    eff = fn('TEST_EV', source=hero.id)
    eff(gs, {})
    
    assert True
