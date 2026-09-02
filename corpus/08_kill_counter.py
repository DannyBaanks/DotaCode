# 08_kill_counter.py — example_1_kill_counter
from gamestate import GameState
from dtypes import Trigger, ActionType
from effects import *
from triggers import *
def setup(gs):

        # Crear dos héroes de equipos opuestos
        hero_a = gs.spawn_entity("hero", {"hp": 100}, (0, 0), {"hero", "team_a"})
        hero_b = gs.spawn_entity("hero", {"hp": 100}, (5, 5), {"hero", "team_b"})

        # Inicializar contadores
        gs.globals["kills_a"] = 0
        gs.globals["kills_b"] = 0

        # Handler: al morir un héroe, incrementar counter del asesino
        def on_death_handler(gs, ctx):
            ev = ctx["event"]
            target = gs.get_entity(ev.target)
            source = gs.get_entity(ev.source)
            if target and target.has_tag("hero") and source and source.has_tag("hero"):
                if source.has_tag("team_a"):
                    gs.globals["kills_a"] = gs.globals.get("kills_a", 0) + 1
                elif source.has_tag("team_b"):
                    gs.globals["kills_b"] = gs.globals.get("kills_b", 0) + 1
            return gs

        t = Trigger(
            id=gs.new_trigger_id(),
            on="ON_DEATH",
            source=hero_a.id,
            then=[on_death_handler],
        )
        gs.add_trigger(t)

        # Matar a hero_b desde hero_a
        emit("ON_DEATH", source=hero_a.id, target=hero_b.id)(gs, {})
