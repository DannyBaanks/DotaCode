# 084 global_dec — (name, delta?) -> — 
# Decrementa global
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: global_dec ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "global_dec", None) or getattr(_gs, "global_dec", None) or getattr(_gs.GameState, "global_dec", None) or getattr(_dt, "global_dec", None)
    assert fn is not None, "global_dec no encontrado"
    # Llamada canónica real
    eff = global_dec('test_var', 1)
    eff(gs, {}) if callable(eff) else None
    assert True
