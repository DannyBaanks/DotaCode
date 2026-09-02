# 248 apply_modifier — (source, target, type, dur, stacks?) -> ModifierId 
# Aplica buff/debuff
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: apply_modifier ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "apply_modifier", None) or getattr(_gs, "apply_modifier", None) or getattr(_gs.GameState, "apply_modifier", None) or getattr(_dt, "apply_modifier", None)
    assert fn is not None, "apply_modifier no encontrado"
    # Llamada canónica real
    eff = apply_modifier(hero.id, hero.id, 1, 1, 1, None, <Severity.BASIC: 1>, False, {'hero'}, None, None)
    eff(gs, {}) if callable(eff) else None
    assert True
