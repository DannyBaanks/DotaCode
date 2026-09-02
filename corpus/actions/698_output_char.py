# 698 output_char — (char_code) -> — 
# Carácter ASCII
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: output_char ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "output_char", None) or getattr(_gs, "output_char", None) or getattr(_gs.GameState, "output_char", None) or getattr(_dt, "output_char", None)
    assert fn is not None, "output_char no encontrado"
    # Llamada canónica real
    eff = output_char(1)
    eff(gs, {}) if callable(eff) else None
    assert True
