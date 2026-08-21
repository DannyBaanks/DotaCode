"""10 ejemplos del megacompose — verificación de MVP.

Cada ejemplo demuestra que las 7 primitivas + runtime pueden construir
comportamientos de Dota 2 sin primitivas adicionales.

Referencia: MEGACOMPOSE §EJEMPLOS
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prng import PRNG
from dtypes import Entity, Modifier, Event, Trigger, EventQueue, ActionType, Severity
from gamestate import GameState
from effects import (
    spawn, destroy, set_alive, set_state, get_state, inc_state, dec_state,
    spend, gain, force_spend, set_resource, get_resource,
    emit, emit_delayed, schedule, periodic, cancel_event,
    apply_modifier, remove_modifier, remove_modifier_type, refresh_modifier, add_stack,
    gate, ungated,
    set_pos, move_to, teleport, distance, in_range,
    output, output_string, output_number,
    set_var, get_var, inc_var, dec_var, global_set, global_get, global_inc,
    seq, branch, each_entity,
)
from triggers import find_matching_triggers, match_event, eval_condition
from runtime import run, run_loop, process_event


# ============================================================================
# 1. Kill Counter
# ============================================================================

def example_1_kill_counter():
    """Cuenta kills por equipo. Cada muerte de héroe incrementa el counter."""
    print("Example 1: Kill Counter")

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

    gs = run(seed=42, setup_fn=setup)
    assert gs.globals["kills_a"] == 1
    assert gs.globals["kills_b"] == 0
    print(f"  kills_a={gs.globals['kills_a']}, kills_b={gs.globals['kills_b']}")
    print("  [PASS]\n")


# ============================================================================
# 2. Cooldown
# ============================================================================

def example_2_cooldown():
    """Habilidad con cooldown: cast → cooldown → re-cast."""
    print("Example 2: Cooldown")

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

    gs = run(seed=42, setup_fn=setup)
    # Solo 1 output = solo 1 cast exitoso
    successful = [o for o in gs.output if o.value == "Fireball cast!"]
    assert len(successful) == 1
    hero = list(gs.entities.values())[0]
    assert hero.state["fireball_cd"] == 5
    assert hero.state["mana"] == 70
    print(f"  cd={hero.state['fireball_cd']}, mana={hero.state['mana']}, casts={len(successful)}")
    print("  [PASS]\n")


# ============================================================================
# 3. Stun temporal
# ============================================================================

def example_3_stun():
    """Stun bloquea acciones por duración determinada."""
    print("Example 3: Stun Temporal")

    def setup(gs):
        hero = gs.spawn_entity("hero", {"mana": 100})
        enemy = gs.spawn_entity("enemy", {"hp": 100})

        # Aplicar STUN al enemy por 3 ticks
        apply_modifier(
            hero.id, enemy.id, "STUN", 3,
            gate={ActionType.MOVE, ActionType.CAST},
        )(gs, {})

        # Intentar castear durante stun
        gs.add_output("OUT_STRING", "attempt1")

    gs = run(seed=42, setup_fn=setup)
    enemy = list(gs.entities.values())[1]
    assert gs.has_modifier_type(enemy.id, "STUN")
    assert gs.is_gated(enemy.id, ActionType.MOVE)
    assert gs.is_gated(enemy.id, ActionType.CAST)
    print(f"  STUN active: {gs.has_modifier_type(enemy.id, 'STUN')}")
    print(f"  MOVE gated: {gs.is_gated(enemy.id, ActionType.MOVE)}")
    print("  [PASS]\n")


# ============================================================================
# 4. Buff con duración
# ============================================================================

def example_4_buff():
    """Buff que modifica un state por duración limitada."""
    print("Example 4: Buff con Duración")

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

        # Emitir 5 ON_TICK para que el modifier ejecute on_tick 4 veces
        for _ in range(5):
            emit("ON_TICK", source=hero.id)(gs, {})

    gs = run(seed=42, setup_fn=setup)
    hero = list(gs.entities.values())[0]
    # After 4 ticks of +1 each: 10 + 4 = 14
    assert hero.state["damage"] == 14
    # Buff should have expired
    assert not gs.has_modifier_type(hero.id, "DAMAGE_BUFF")
    print(f"  damage={hero.state['damage']}, buff_active={gs.has_modifier_type(hero.id, 'DAMAGE_BUFF')}")
    print("  [PASS]\n")


# ============================================================================
# 5. Projectile
# ============================================================================

def example_5_projectile():
    """Proyectil que viaja y aplica daño al impactar."""
    print("Example 5: Projectile")

    def setup(gs):
        caster = gs.spawn_entity("caster", {"mana": 100}, (0, 0))
        target = gs.spawn_entity("target", {"hp": 100}, (5, 0))

        # Spawn projectile que viaja hacia target
        proj = gs.spawn_entity("projectile", {"damage": 25, "speed": 2}, (0, 0), {"projectile"})

        # Movimiento periódico del proyectil
        def move_projectile(gs, ctx):
            p = gs.get_entity(proj.id)
            t = gs.get_entity(target.id)
            if p and t and p.alive and t.alive:
                # Mover 2 unidades hacia target
                dx = t.position[0] - p.position[0]
                if abs(dx) <= p.state["speed"]:
                    # Impacto!
                    t.state["hp"] -= p.state["damage"]
                    gs.add_output("OUT_STRING", f"Hit for {p.state['damage']}")
                    gs.destroy_entity(p.id)
                else:
                    p.position = (p.position[0] + p.state["speed"], p.position[1])
            return gs

        periodic(move_projectile, every=1)(gs, {})

    gs = run(seed=42, setup_fn=setup, max_ticks=20)
    # Proyectil debió impactar en ~3 ticks (dist=5, speed=2)
    hits = [o for o in gs.output if "Hit" in str(o.value)]
    assert len(hits) >= 1
    # Target debió recibir daño
    target = [e for e in gs.entities.values() if e.type == "target"][0]
    assert target.state["hp"] == 75
    print(f"  target_hp={target.state['hp']}, hits={len(hits)}")
    print("  [PASS]\n")


# ============================================================================
# 6. Área de efecto (AoE)
# ============================================================================

def example_6_aoe():
    """Daño de área que afecta todas las entities en radio."""
    print("Example 6: Area of Effect")

    def setup(gs):
        caster = gs.spawn_entity("caster", {"mana": 100}, (0, 0))

        # Spawn múltiples targets
        t1 = gs.spawn_entity("target", {"hp": 100}, (2, 0), {"target"})
        t2 = gs.spawn_entity("target", {"hp": 100}, (3, 1), {"target"})
        t3 = gs.spawn_entity("target", {"hp": 100}, (10, 10), {"target"})  # fuera de rango

        # AoE: dañar a todos en radio 5 desde caster
        def aoe_damage(gs, ctx):
            center = gs.get_entity(caster.id).position
            for e in gs.alive_entities():
                if e.has_tag("target"):
                    dist = abs(e.position[0] - center[0]) + abs(e.position[1] - center[1])
                    if dist <= 5:
                        e.state["hp"] -= 30
            return gs

        aoe_damage(gs, {})

    gs = run(seed=42, setup_fn=setup)
    targets = [e for e in gs.entities.values() if e.type == "target"]
    # t1 (dist=2) y t2 (dist=4) debieron recibir daño
    # t3 (dist=20) no
    assert targets[0].state["hp"] == 70  # t1
    assert targets[1].state["hp"] == 70  # t2
    assert targets[2].state["hp"] == 100  # t3 fuera de rango
    print(f"  t1_hp={targets[0].state['hp']}, t2_hp={targets[1].state['hp']}, t3_hp={targets[2].state['hp']}")
    print("  [PASS]\n")


# ============================================================================
# 7. Resource Loop
# ============================================================================

def example_7_resource_loop():
    """Regeneración de mana cada tick hasta el máximo."""
    print("Example 7: Resource Loop")

    def setup(gs):
        hero = gs.spawn_entity("hero", {"mana": 20, "mana_max": 100, "mana_regen": 10})
        # Emitir ticks para que regen se ejecute
        for _ in range(10):
            emit("ON_TICK", source=hero.id)(gs, {})

    gs = run(seed=42, setup_fn=setup, max_ticks=20)
    hero = list(gs.entities.values())[0]
    # 20 + 10*8 = 100 (capped at max after 8 ticks)
    assert hero.state["mana"] == 100
    print(f"  mana={hero.state['mana']} (capped at max)")
    print("  [PASS]\n")


# ============================================================================
# 8. Combo de habilidades
# ============================================================================

def example_8_combo():
    """Combo: stun → damage amplificado → finish."""
    print("Example 8: Combo de Habilidades")

    def setup(gs):
        hero = gs.spawn_entity("hero", {"mana": 100, "combo_ready": True})
        enemy = gs.spawn_entity("enemy", {"hp": 100})

        # Combo: si enemy está stuneado, daño x2
        def combo_damage(gs, ctx):
            e = gs.get_entity(enemy.id)
            if e and gs.has_modifier_type(enemy.id, "STUN"):
                e.state["hp"] -= 60  # Daño amplificado
                gs.add_output("OUT_STRING", "Combo hit!")
            elif e:
                e.state["hp"] -= 30  # Daño normal
                gs.add_output("OUT_STRING", "Normal hit")
            return gs

        # Paso 1: Aplicar stun
        apply_modifier(hero.id, enemy.id, "STUN", 3,
                       gate={ActionType.MOVE, ActionType.CAST})(gs, {})

        # Paso 2: Ejecutar combo (stun activo → daño x2)
        combo_damage(gs, {})

    gs = run(seed=42, setup_fn=setup)
    enemy = [e for e in gs.entities.values() if e.type == "enemy"][0]
    assert enemy.state["hp"] == 40  # 100 - 60
    combo_hits = [o for o in gs.output if o.value == "Combo hit!"]
    assert len(combo_hits) == 1
    print(f"  enemy_hp={enemy.state['hp']}, combo_hits={len(combo_hits)}")
    print("  [PASS]\n")


# ============================================================================
# 9. Item + Ability
# ============================================================================

def example_9_item_ability():
    """Item que reduce cooldown + habilidad que lo usa."""
    print("Example 9: Item + Ability")

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

    gs = run(seed=42, setup_fn=setup)
    hero = list(gs.entities.values())[0]
    assert hero.state["fireball_cd"] == 3  # 5 - 2 = 3
    assert hero.state["cd_reduction"] == 2
    print(f"  cd={hero.state['fireball_cd']}, reduction={hero.state['cd_reduction']}")
    print("  [PASS]\n")


# ============================================================================
# 10. Pequeña simulación completa
# ============================================================================

def example_10_simulation():
    """Simulación: 2 héroes, resources, combate, muerte, respawn."""
    print("Example 10: Simulación Completa")

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

    gs = run(seed=42, setup_fn=setup, max_ticks=50)

    # Verificar resultados
    deaths = gs.globals.get("death_count", 0)
    hero_b = [e for e in gs.entities.values() if e.type == "hero" and e.has_tag("team_b")][0]
    respawn_msgs = [o for o in gs.output if "respawned" in str(o.value)]

    assert deaths >= 1
    assert hero_b.alive  # respawned
    assert hero_b.state["hp"] == hero_b.state.get("hp_max", 80)
    print(f"  deaths={deaths}, hero_b_alive={hero_b.alive}, hp={hero_b.state['hp']}")
    print(f"  respawn_messages={len(respawn_msgs)}")
    print("  [PASS]\n")


# ============================================================================
# Run all examples
# ============================================================================

def main():
    print("=== DotaCode — 10 Ejemplos del Megacompose ===\n")

    example_1_kill_counter()
    example_2_cooldown()
    example_3_stun()
    example_4_buff()
    example_5_projectile()
    example_6_aoe()
    example_7_resource_loop()
    example_8_combo()
    example_9_item_ability()
    example_10_simulation()

    print("=== ALL 10 EXAMPLES PASSED ===")


if __name__ == "__main__":
    main()
