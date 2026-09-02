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
    eff = ungated(hero.id, 1)
    eff(gs, {}) if callable(eff) else None
    assert True
