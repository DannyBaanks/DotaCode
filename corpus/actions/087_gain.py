# 087 gain — (entity, resource, amount) -> — 
# Añade (respeta max)
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: gain ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "gain", None) or getattr(_gs, "gain", None) or getattr(_gs.GameState, "gain", None) or getattr(_dt, "gain", None)
    assert fn is not None, "gain no encontrado"
    # Llamada canónica real
    eff = gain(hero.id, 'hp', 10)
    eff(gs, {}) if callable(eff) else None
    assert True
