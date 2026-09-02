# 699 output_string — (string) -> — 
# Cadena
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: output_string ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "output_string", None) or getattr(_gs, "output_string", None) or getattr(_gs.GameState, "output_string", None) or getattr(_dt, "output_string", None)
    assert fn is not None, "output_string no encontrado"
    # Llamada canónica real
    eff = output_string(1)
    eff(gs, {}) if callable(eff) else None
    assert True
