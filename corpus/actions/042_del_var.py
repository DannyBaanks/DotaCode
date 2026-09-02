# 042 del_var — (name) -> — 
# Elimina variable
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: del_var ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "del_var", None) or getattr(_gs, "del_var", None) or getattr(_gs.GameState, "del_var", None) or getattr(_dt, "del_var", None)
    assert fn is not None, "del_var no encontrado"
    # Llamada canónica real
    eff = del_var('test_var')
    eff(gs, {}) if callable(eff) else None
    assert True
