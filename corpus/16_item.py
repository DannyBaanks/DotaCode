# 16_item.py — example_9_item_ability
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        hero = gs.spawn_entity("hero", {"mana": 100, "fireball_cd": 0, "cd_reduction": 0})

        # Item: reduce cooldown en 2 ticks
        def apply_item(gs, ctx):
            e = gs.get_entity(hero.id)
            if e:
                e.state["cd_reduction"] = 2
            return gs

        # Habilidad: cast con cooldown reducido
        def on_cast(gs, ctx):
            e = gs.get_entity(hero.id)
            if e and e.state.get("fireball_cd", 0) <= 0:
                cd = max(1, 5 - e.state.get("cd_reduction", 0))  # 5 - 2 = 3
                e.state["fireball_cd"] = cd
                gs.add_output("OUT_STRING", f"Cast! cd={cd}")
            return gs

        t = Trigger(id=gs.new_trigger_id(), on="ON_CAST", source=hero.id, then=[on_cast])
        gs.add_trigger(t)

        # Aplicar item
        apply_item(gs, {})

        # Castear
        emit("ON_CAST", source=hero.id)(gs, {})
