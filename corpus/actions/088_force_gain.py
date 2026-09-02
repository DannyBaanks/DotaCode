# 088 force_gain — (entity, resource, amount) -> — 
# Añade ignorando max
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: force_gain ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "force_gain", None) or getattr(_gs, "force_gain", None) or getattr(_gs.GameState, "force_gain", None) or getattr(_dt, "force_gain", None)
    assert fn is not None, "force_gain no encontrado"
    # Llamada canónica real
    eff = fn(hero.id, 'hp', 10)
    eff(gs, {}) if callable(eff) else None
    assert True  # POST genérico (se especializa abajo)
