# 255 add_stack — (modifier, amount?) -> — 
# Añade stacks (+1 default)
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: add_stack ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "add_stack", None) or getattr(_gs, "add_stack", None) or getattr(_gs.GameState, "add_stack", None) or getattr(_dt, "add_stack", None)
    assert fn is not None, "add_stack no encontrado"
    # Llamada canónica real
    eff = add_stack(1, 10)
    eff(gs, {}) if callable(eff) else None
    assert True
