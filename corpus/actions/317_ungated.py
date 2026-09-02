# 317 ungated — (target, action_type) -> — 
# Desbloquea categoría
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: ungated ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "ungated", None) or getattr(_gs, "ungated", None) or getattr(_gs.GameState, "ungated", None) or getattr(_dt, "ungated", None)
    assert fn is not None, "ungated no encontrado"
    # Llamada canónica real
    from dtypes import ActionType
    import effects as _e2
    _e2.gate(hero.id, {ActionType.MOVE}, 5)(gs, {})
    eff = fn(hero.id, ActionType.MOVE)
    eff(gs, {})
    
    assert not gs.is_gated(hero.id, ActionType.MOVE)
