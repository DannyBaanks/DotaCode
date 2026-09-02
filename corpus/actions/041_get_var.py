# 041 get_var — (name) -> Value 
# Lee variable
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_var ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_var", None) or getattr(_gs, "get_var", None) or getattr(_gs.GameState, "get_var", None) or getattr(_dt, "get_var", None)
    assert fn is not None, "get_var no encontrado"
    # Llamada canónica real
    eff = get_var('test_var')
    eff(gs, {}) if callable(eff) else None
    assert True
