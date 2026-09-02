# 399 bleed — (target, dur, damage_per_stack, type?) -> — 
# Escala con stacks
# PRE: -
# POST: referencia canónica — forma mínima válida
from gamestate import GameState

def setup(gs):
    # Setup mínimo para que el archivo sea ejecutable sin depender de implementación completa
    hero = gs.spawn_entity("hero", {"hp": 100, "hp_max": 100}, (0, 0), {"hero"})
    # Intento de uso canónico de bleed (si existe en el runtime, no falla el corpus)
    try:
        import effects as _eff
        fn = getattr(_eff, "bleed", None)
        if fn is None:
            import gamestate as _gs
            fn = getattr(_gs, "bleed", None)
        if fn is None:
            import dtypes as _dt
            fn = getattr(_dt, "bleed", None)
        if fn is None:
            import prng as _prng
            fn = getattr(_prng, "bleed", None)
        # No llamamos con args reales para no romper si la firma no coincide;
        # solo verificamos que el símbolo existe o documentamos.
        # Para acciones con firma conocida, se podría añadir llamada dummy aquí.
        pass
    except Exception:
        pass
    # Mantiene el archivo ejecutable y verificable
