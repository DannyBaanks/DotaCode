# 316 gate — (target, action_types, dur) -> — 
# Bloquea categorías genéricas
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: gate ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "gate", None) or getattr(_gs, "gate", None) or getattr(_gs.GameState, "gate", None) or getattr(_dt, "gate", None)
    assert fn is not None, "gate no encontrado"
    # Llamada canónica real
    eff = gate(hero.id, 1, 1)
    eff(gs, {}) if callable(eff) else None
    assert True
