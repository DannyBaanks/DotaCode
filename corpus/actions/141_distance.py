# 141 distance — (a, b) -> Int 
# Manhattan/euclidiana (decidir)
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: distance ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "distance", None) or getattr(_gs, "distance", None) or getattr(_gs.GameState, "distance", None) or getattr(_dt, "distance", None)
    assert fn is not None, "distance no encontrado"
    # Llamada canónica real
    hero2 = gs.spawn_entity('dummy', {}, (3,4))
    eff = fn(hero.id, hero2.id)
    ctx={}
    eff(gs, ctx)
    
    assert ctx.get('result') == 7
