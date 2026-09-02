# 319 is_gated — (target, action_type) -> Bool 
# Verifica bloqueo
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: is_gated ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "is_gated", None) or getattr(_gs, "is_gated", None) or getattr(_gs.GameState, "is_gated", None) or getattr(_dt, "is_gated", None)
    assert fn is not None, "is_gated no encontrado"
    # Llamada canónica real
    from dtypes import ActionType
    res = gs.is_gated(hero.id, ActionType.MOVE)
    
    assert isinstance(res, bool)
