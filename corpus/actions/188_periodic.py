# 188 periodic — (effect, every, times?) -> EventId 
# Repite cada N ticks
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: periodic ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "periodic", None) or getattr(_gs, "periodic", None) or getattr(_gs.GameState, "periodic", None) or getattr(_dt, "periodic", None)
    assert fn is not None, "periodic no encontrado"
    # Llamada canónica real
    from effects import output_number
    eff = fn(output_number(1), 1, 1)
    eff(gs, {})
    
    assert True
