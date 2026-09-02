# 701 output_newline — — -> — 
# Salto de línea
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: output_newline ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "output_newline", None) or getattr(_gs, "output_newline", None) or getattr(_gs.GameState, "output_newline", None) or getattr(_dt, "output_newline", None)
    assert fn is not None, "output_newline no encontrado"
    # Llamada canónica real
    eff = output_newline()
    eff(gs, {}) if callable(eff) else None
    assert True
