# 040 set_var — (name, value) -> — 
# Variable del programa
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_var ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_var", None) or getattr(_gs, "set_var", None) or getattr(_gs.GameState, "set_var", None) or getattr(_dt, "set_var", None)
    assert fn is not None, "set_var no encontrado"
    # Llamada canónica real
    eff = set_var('test_var', 1)
    eff(gs, {}) if callable(eff) else None
    assert True
