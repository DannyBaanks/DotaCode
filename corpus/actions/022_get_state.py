# 022 get_state — (entity, key) -> Value 
# Lee valor del state
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_state", None) or getattr(_gs, "get_state", None) or getattr(_gs.GameState, "get_state", None) or getattr(_dt, "get_state", None)
    assert fn is not None, "get_state no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp')
    ctx={}
    eff(gs, ctx)
    
    assert ctx.get('result') == 100
