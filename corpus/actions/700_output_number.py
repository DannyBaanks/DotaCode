# 700 output_number — (number) -> — 
# Número
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: output_number ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "output_number", None) or getattr(_gs, "output_number", None) or getattr(_gs.GameState, "output_number", None) or getattr(_dt, "output_number", None)
    assert fn is not None, "output_number no encontrado"
    # Llamada canónica real
    eff = fn(42)
    eff(gs, {})
    
    assert gs.output[-1].value == 42
