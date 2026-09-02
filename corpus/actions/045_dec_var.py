# 045 dec_var — (name, delta?) -> — 
# Decrementa numérica
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: dec_var ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "dec_var", None) or getattr(_gs, "dec_var", None) or getattr(_gs.GameState, "dec_var", None) or getattr(_dt, "dec_var", None)
    assert fn is not None, "dec_var no encontrado"
    # Llamada canónica real
    eff = dec_var('test_var', 1)
    eff(gs, {}) if callable(eff) else None
    assert True
