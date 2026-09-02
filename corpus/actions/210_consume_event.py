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
    from dtypes import Event
    ev = Event(id=gs.new_event_id(), tick=0, type='TEST', source=hero.id)
    eff = fn(ev)
    eff(gs, {})
    
    assert ev.consumed
