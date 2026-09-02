# 144 in_range — (source, target, range) -> Bool 
# Distancia <= range
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: in_range ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "in_range", None) or getattr(_gs, "in_range", None) or getattr(_gs.GameState, "in_range", None) or getattr(_dt, "in_range", None)
    assert fn is not None, "in_range no encontrado"
    # Llamada canónica real
    hero2 = gs.spawn_entity('dummy', {}, (1,0))
    eff = fn(hero.id, hero2.id, 5)
    ctx={}
    eff(gs, ctx)
    
    assert ctx.get('result') == True
