# 044 inc_var — (name, delta?) -> — 
# Incrementa numérica
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: inc_var ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "inc_var", None) or getattr(_gs, "inc_var", None) or getattr(_gs.GameState, "inc_var", None) or getattr(_dt, "inc_var", None)
    assert fn is not None, "inc_var no encontrado"
    # Llamada canónica real
    fn('test_var', 5)(gs, {})
    eff = fn('test_var', 2)
    eff(gs, {})
    
    assert gs.vars.get('test_var') == 7
