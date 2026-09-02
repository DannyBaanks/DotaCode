# 120 move_to — (entity, x, y) -> — 
# Mueve instantáneamente
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: move_to ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "move_to", None) or getattr(_gs, "move_to", None) or getattr(_gs.GameState, "move_to", None) or getattr(_dt, "move_to", None)
    assert fn is not None, "move_to no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 7, 8)
    eff(gs, {})
    
    assert hero.position == (7,8)
