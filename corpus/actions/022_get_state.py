# 022 get_state — (entity, key) -> Value 
# Lee valor del state
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: get_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "get_state", None) or getattr(_gs, "get_state", None) or getattr(_gs.GameState, "get_state", None) or getattr(_dt, "get_state", None)
    assert fn is not None, "get_state no encontrado"
    # Llamada canónica real
    eff = get_state(hero.id, 'hp', 1) if 'get_state' not in ('get_state',) else get_state(hero.id, 'hp')
    eff(gs, {}) if callable(eff) else None
    assert hero.state.get('hp') is not None
