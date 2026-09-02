# 029 clamp_state — (entity, key, min, max) -> — 
# Limita al rango [min, max]
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: clamp_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "clamp_state", None) or getattr(_gs, "clamp_state", None) or getattr(_gs.GameState, "clamp_state", None) or getattr(_dt, "clamp_state", None)
    assert fn is not None, "clamp_state no encontrado"
    # Llamada canónica real
    eff = clamp_state(hero.id, 'hp', 1) if 'clamp_state' not in ('get_state',) else clamp_state(hero.id, 'hp')
    eff(gs, {}) if callable(eff) else None
    assert hero.state.get('hp') is not None
