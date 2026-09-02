# 082 global_get — (name) -> Value 
# Lee global
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: global_get ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "global_get", None) or getattr(_gs, "global_get", None) or getattr(_gs.GameState, "global_get", None) or getattr(_dt, "global_get", None)
    assert fn is not None, "global_get no encontrado"
    # Llamada canónica real
    import effects as _e2
    _e2.global_set('gtest', 55)(gs, {})
    eff = fn('gtest')
    ctx={}
    eff(gs, ctx)
    
    assert ctx.get('result') == 55
