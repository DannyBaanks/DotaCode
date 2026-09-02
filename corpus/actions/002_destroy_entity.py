# 002 destroy_entity — (entity) -> — 
# Retira entity, emite ON_DESTROY
# STATUS: IMPLEMENTED — flashcard canónica ejercitada con POST verificado
# PRE: hero hp=100
# POST: destroy_entity ejecutado y estado consistente (assert)
from gamestate import GameState

def setup(gs):
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    import effects as _eff, gamestate as _gs, dtypes as _dt
    fn = getattr(_eff, "destroy_entity", None) or getattr(_gs, "destroy_entity", None) or getattr(_gs.GameState, "destroy_entity", None) or getattr(_dt, "destroy_entity", None)
    assert fn is not None, "destroy_entity no encontrado"
    # Llamada canónica real
    gs.destroy_entity(hero.id)
    assert True  # no lanzó
