# 11_buff.py — example_4_buff
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"damage": 10})

        # Aplicar buff +1 damage por 4 ticks
        def on_tick(gs, ctx):
            e = gs.get_entity(ctx["target"])
            if e:
                e.state["damage"] = e.state.get("damage", 0) + 1
            return gs

        apply_modifier(
            hero.id, hero.id, "DAMAGE_BUFF", 4,
            on_tick=on_tick,
            tags={"buff"},
        )(gs, {})

        # Un evento futuro hace avanzar el reloj cinco veces; el buff recibe
        # cuatro ticks antes de expirar. Eventos en tick 0 no consumen tiempo.
        emit_delayed("ON_TICK", 5, source=hero.id)(gs, {})
