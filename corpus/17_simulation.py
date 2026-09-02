# 17_simulation.py — example_10_simulation
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        # Crear mundo
        gs.globals["tick_count"] = 0
        gs.globals["death_count"] = 0

        # Héroes
        hero_a = gs.spawn_entity("hero", {
            "hp": 100, "hp_max": 100,
            "mana": 50, "mana_max": 100,
            "mana_regen": 5,
            "damage": 25,
        }, (0, 0), {"hero", "team_a"})

        hero_b = gs.spawn_entity("hero", {
            "hp": 80, "hp_max": 80,
            "mana": 30, "mana_max": 80,
            "mana_regen": 3,
            "damage": 20,
        }, (3, 0), {"hero", "team_b"})

        # Handler: cada ON_TICK incrementa counter
        def tick_handler(gs, ctx):
            gs.globals["tick_count"] = gs.globals.get("tick_count", 0) + 1
            return gs

        t_tick = Trigger(id=gs.new_trigger_id(), on="ON_TICK", source=hero_a.id, then=[tick_handler])
        gs.add_trigger(t_tick)

        # Handler: al recibir daño letal, morir
        def damage_handler(gs, ctx):
            ev = ctx["event"]
            target = gs.get_entity(ev.target)
            if target and target.state.get("hp", 0) <= 0 and target.alive:
                target.alive = False
                gs.globals["death_count"] = gs.globals.get("death_count", 0) + 1
                gs.add_output("OUT_STRING", f"{target.type} died!")
                # Respawn después de 5 ticks
                def respawn(gs, ctx):
                    t = gs.get_entity(target.id)
                    if t:
                        t.alive = True
                        t.state["hp"] = t.state.get("hp_max", 100)
                        t.state["mana"] = t.state.get("mana_max", 100)
                        gs.add_output("OUT_STRING", f"{t.type} respawned!")
                    return gs
                schedule(respawn, 5)(gs, ctx)
            return gs

        t_dmg = Trigger(id=gs.new_trigger_id(), on="ON_DAMAGE", source=hero_a.id, then=[damage_handler])
        gs.add_trigger(t_dmg)

        # Simular combate: hero_a ataca a hero_b 4 veces
        for _ in range(4):
            def attack(gs, ctx):
                target = gs.get_entity(hero_b.id)
                if target and target.alive:
                    target.state["hp"] -= 25
                    gs.add_trace(ctx.get("event_id", 0), "ATTACK", hero_a.id, hero_b.id,
                                 hero_b.id, {"hp": target.state["hp"] + 25}, "damage",
                                 {"hp": target.state["hp"]})
                    emit("ON_DAMAGE", source=hero_a.id, target=hero_b.id,
                         payload={"amount": 25})(gs, ctx)
                return gs
            attack(gs, {})

        # Tick para respawn
        for _ in range(8):
            emit("ON_TICK", source=hero_a.id)(gs, {})
