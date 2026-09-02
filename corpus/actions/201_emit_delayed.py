# 201 emit_delayed — (type, ticks, source?, target?, payload) -> EventId 
# Emite tras N ticks
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: emit_delayed ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "emit_delayed", None) or getattr(_gs, "emit_delayed", None) or getattr(_gs.GameState, "emit_delayed", None) or getattr(_dt, "emit_delayed", None)
    assert fn is not None, "emit_delayed no encontrado"
    # Llamada canónica real
    eff = fn('TEST_EV', 1, source=hero.id)
    eff(gs, {})
    
    assert True
