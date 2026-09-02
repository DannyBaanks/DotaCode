# 09_cooldown.py — example_2_cooldown
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"mana": 100, "fireball_cd": 0})

        # Trigger ON_CAST: si cooldown=0 y mana>=30, gastar mana y poner cooldown
        def on_cast(gs, ctx):
            ev = ctx["event"]
            e = gs.get_entity(ev.source)
            if e and e.state.get("fireball_cd", 0) <= 0 and e.state.get("mana", 0) >= 30:
                e.state["mana"] -= 30
                e.state["fireball_cd"] = 5
                gs.add_output("OUT_STRING", "Fireball cast!")
            return gs

        t = Trigger(id=gs.new_trigger_id(), on="ON_CAST", source=hero.id, then=[on_cast])
        gs.add_trigger(t)

        # Intentar castear 3 veces
        emit("ON_CAST", source=hero.id)(gs, {})  # OK (cd=0)
        emit("ON_CAST", source=hero.id)(gs, {})  # FAIL (cd=5)
        emit("ON_CAST", source=hero.id)(gs, {})  # FAIL (cd=5)
