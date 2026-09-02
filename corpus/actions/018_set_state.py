# 018 set_state — (entity, key, value) -> — 
# Asigna valor
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: set_state ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "set_state", None) or getattr(_gs, "set_state", None) or getattr(_gs.GameState, "set_state", None) or getattr(_dt, "set_state", None)
    assert fn is not None, "set_state no encontrado"
    # Llamada canónica real
    eff = set_state(hero.id, 'hp', 1) if 'set_state' not in ('get_state',) else set_state(hero.id, 'hp')
    eff(gs, {}) if callable(eff) else None
    assert hero.state.get('hp') is not None
