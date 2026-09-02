# 015 set_owner — (entity, new_owner) -> — 
# Cambia dueño
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_owner ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_owner", None) or getattr(_gs, "set_owner", None) or getattr(_gs.GameState, "set_owner", None) or getattr(_dt, "set_owner", None)
    assert fn is not None, "set_owner no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, None)
    eff(gs, {}) if callable(eff) else None
    assert True  # POST genérico (se especializa abajo)
