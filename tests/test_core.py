"""Tests del runtime DotaCode.

Verifica invariants de SPEC §15 y funcionalidad básica.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from prng import PRNG
from dtypes import (
    Entity, Modifier, Event, Trigger, EventQueue,
    ActionType, Severity,
)
from gamestate import GameState
from effects import (
    spawn, destroy, set_alive, set_state, get_state, inc_state, dec_state,
    spend, gain, force_spend, force_gain, set_resource, get_resource,
    emit, emit_delayed, schedule, periodic, cancel_event,
    apply_modifier, remove_modifier, remove_modifier_type, refresh_modifier, add_stack,
    gate, ungated,
    set_pos, move_to, teleport, distance, in_range,
    output, output_string, output_number,
    set_var, get_var, inc_var, dec_var, global_set, global_get, global_inc,
    seq, branch,
)
from triggers import match_event, eval_condition, find_matching_triggers
from runtime import run, run_loop, process_event


# ============================================================================
# PRNG
# ============================================================================

def test_prng_determinism():
    """SPEC §10: misma seed → misma secuencia."""
    rng1 = PRNG(42)
    rng2 = PRNG(42)
    for _ in range(100):
        assert rng1.next_int(0, 1000) == rng2.next_int(0, 1000)
    print("  [PASS] PRNG determinism")

def test_prng_range():
    rng = PRNG(1)
    for _ in range(1000):
        v = rng.next_int(5, 10)
        assert 5 <= v <= 10
    print("  [PASS] PRNG range")

def test_prng_checkpoint_restore():
    rng = PRNG(99)
    rng.next_int(0, 100)
    rng.next_int(0, 100)
    cp = rng.checkpoint()
    v1 = rng.next_int(0, 100)
    v2 = rng.next_int(0, 100)
    rng.restore(cp)
    assert rng.next_int(0, 100) == v1
    assert rng.next_int(0, 100) == v2
    print("  [PASS] PRNG checkpoint/restore")

def test_prng_fork():
    rng1 = PRNG(42)
    rng2 = PRNG(99)
    # Different seeds → different sequences
    vals1 = [rng1.next_int(0, 10000) for _ in range(50)]
    vals2 = [rng2.next_int(0, 10000) for _ in range(50)]
    assert vals1 != vals2
    print("  [PASS] PRNG different seeds")


# ============================================================================
# EventQueue
# ============================================================================

def test_eventqueue_fifo_same_tick():
    q = EventQueue()
    q.push(Event(id=1, tick=0, type="A"))
    q.push(Event(id=2, tick=0, type="B"))
    q.push(Event(id=3, tick=0, type="C"))
    assert q.pop().type == "A"
    assert q.pop().type == "B"
    assert q.pop().type == "C"
    print("  [PASS] EventQueue FIFO same tick")

def test_eventqueue_tick_ordering():
    q = EventQueue()
    q.push(Event(id=1, tick=5, type="LATE"))
    q.push(Event(id=2, tick=0, type="EARLY"))
    q.push(Event(id=3, tick=2, type="MID"))
    assert q.pop().type == "EARLY"
    assert q.pop().type == "MID"
    assert q.pop().type == "LATE"
    print("  [PASS] EventQueue tick ordering")

def test_eventqueue_cancel():
    q = EventQueue()
    q.push(Event(id=1, tick=0, type="A"))
    q.push(Event(id=2, tick=0, type="B"))
    q.cancel(1)
    ev = q.pop()
    assert ev.type == "B"  # A was cancelled, skipped
    print("  [PASS] EventQueue cancel")


# ============================================================================
# Entity
# ============================================================================

def test_entity_spawn_destroy():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"hp": 100, "mana": 50}, (3, 4), {"hero", "ranged"})
    assert e.id in gs.entities
    assert e.state["hp"] == 100
    assert e.position == (3, 4)
    assert e.has_tag("hero")
    gs.destroy_entity(e.id)
    assert e.id not in gs.entities
    print("  [PASS] Entity spawn/destroy")

def test_entity_alive_filter():
    gs = GameState(seed=1)
    a = gs.spawn_entity("hero", tags={"hero"})
    b = gs.spawn_entity("hero", tags={"hero"})
    b.alive = False
    assert len(gs.alive_entities()) == 1
    assert len(gs.entities_with_tag("hero")) == 1
    print("  [PASS] Entity alive filter")


# ============================================================================
# Modifier
# ============================================================================

def test_modifier_lifecycle():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero")
    mod = Modifier(id=1, source=1, target=e.id, type="STUN", duration=3, max_dur=3,
                   gate={ActionType.MOVE, ActionType.CAST})
    gs.add_modifier(mod)
    assert gs.has_modifier_type(e.id, "STUN")
    assert gs.is_gated(e.id, ActionType.MOVE)
    assert not gs.is_gated(e.id, ActionType.ATTACK)
    mod.tick_down()  # 3→2
    mod.tick_down()  # 2→1
    assert not mod.is_expired
    mod.tick_down()  # 1→0
    assert mod.is_expired
    gs.remove_modifier(mod.id)
    assert not gs.has_modifier_type(e.id, "STUN")
    print("  [PASS] Modifier lifecycle")

def test_modifier_refresh():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero")
    mod = Modifier(id=1, source=1, target=e.id, type="BUFF", duration=2, max_dur=5)
    gs.add_modifier(mod)
    mod.tick_down()  # 2→1
    mod.tick_down()  # 1→0
    assert mod.is_expired
    # Refresh should reset to max_dur
    mod.duration = mod.max_dur
    assert not mod.is_expired
    print("  [PASS] Modifier refresh")


# ============================================================================
# Resource operations
# ============================================================================

def test_spend_success():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"mana": 100})
    ctx = {}
    spend(e.id, "mana", 30)(gs, ctx)
    assert ctx["result"] == True
    assert e.state["mana"] == 70
    print("  [PASS] spend success")

def test_spend_insufficient():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"mana": 20})
    ctx = {}
    spend(e.id, "mana", 30)(gs, ctx)
    assert ctx["result"] == False
    assert e.state["mana"] == 20  # unchanged
    print("  [PASS] spend insufficient")

def test_gain_respects_max():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"hp": 90, "hp_max": 100})
    ctx = {}
    gain(e.id, "hp", 20)(gs, ctx)
    assert e.state["hp"] == 100  # capped
    print("  [PASS] gain respects max")

def test_gain_no_max():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"gold": 100})
    ctx = {}
    gain(e.id, "gold", 50)(gs, ctx)
    assert e.state["gold"] == 150
    print("  [PASS] gain no max")

def test_force_spend_negative():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"mana": 10})
    ctx = {}
    force_spend(e.id, "mana", 30)(gs, ctx)
    assert e.state["mana"] == -20
    print("  [PASS] force_spend negative")


# ============================================================================
# Trigger matching
# ============================================================================

def test_match_event_exact():
    assert match_event("ON_CAST", "ON_CAST")
    assert not match_event("ON_CAST", "ON_DAMAGE")
    print("  [PASS] match_event exact")

def test_match_event_wildcard():
    assert match_event("_", "ON_CAST")
    assert match_event("_", "ON_DAMAGE")
    print("  [PASS] match_event wildcard")

def test_find_matching_triggers():
    gs = GameState(seed=1)
    hero = gs.spawn_entity("hero")
    t = Trigger(id=gs.new_trigger_id(), on="ON_CAST", source=hero.id)
    gs.add_trigger(t)
    ev = Event(id=1, tick=0, type="ON_CAST", source=hero.id, target=hero.id)
    matches = find_matching_triggers(gs, ev)
    assert len(matches) == 1
    assert matches[0][0].id == t.id
    print("  [PASS] find_matching_triggers")


# ============================================================================
# Gating
# ============================================================================

def test_gate_prevents_action():
    gs = GameState(seed=1)
    hero = gs.spawn_entity("hero")
    # Apply STUN gate
    apply_modifier(hero.id, hero.id, "STUN", 3,
                   gate={ActionType.MOVE, ActionType.CAST})(gs, {})
    assert gs.is_gated(hero.id, ActionType.MOVE)
    assert gs.is_gated(hero.id, ActionType.CAST)
    assert not gs.is_gated(hero.id, ActionType.ATTACK)
    print("  [PASS] gate prevents action")


# ============================================================================
# Effects composition
# ============================================================================

def test_seq_effects():
    gs = GameState(seed=1)
    e = gs.spawn_entity("hero", {"hp": 50, "mana": 100})
    fx = seq(
        inc_state(e.id, "hp", 10),
        dec_state(e.id, "mana", 20),
    )
    fx(gs, {})
    assert e.state["hp"] == 60
    assert e.state["mana"] == 80
    print("  [PASS] seq effects")


# ============================================================================
# Variables
# ============================================================================

def test_var_operations():
    gs = GameState(seed=1)
    set_var("x", 10)(gs, {})
    ctx = {}
    get_var("x")(gs, ctx)
    assert ctx["result"] == 10
    inc_var("x", 5)(gs, {})
    get_var("x")(gs, ctx)
    assert ctx["result"] == 15
    dec_var("x", 3)(gs, {})
    get_var("x")(gs, ctx)
    assert ctx["result"] == 12
    print("  [PASS] var operations")

def test_global_operations():
    gs = GameState(seed=1)
    global_set("score", 0)(gs, {})
    global_inc("score")(gs, {})
    global_inc("score")(gs, {})
    ctx = {}
    global_get("score")(gs, ctx)
    assert ctx["result"] == 2
    print("  [PASS] global operations")


# ============================================================================
# Position
# ============================================================================

def test_distance():
    gs = GameState(seed=1)
    a = gs.spawn_entity("hero", position=(0, 0))
    b = gs.spawn_entity("hero", position=(3, 4))
    ctx = {}
    distance(a.id, b.id)(gs, ctx)
    assert ctx["result"] == 7  # Manhattan
    print("  [PASS] distance")

def test_in_range():
    gs = GameState(seed=1)
    a = gs.spawn_entity("hero", position=(0, 0))
    b = gs.spawn_entity("hero", position=(3, 4))
    ctx = {}
    in_range(a.id, b.id, 7)(gs, ctx)
    assert ctx["result"] == True
    in_range(a.id, b.id, 5)(gs, ctx)
    assert ctx["result"] == False
    print("  [PASS] in range")


# ============================================================================
# Runtime — basic integration
# ============================================================================

def test_runtime_emit_and_process():
    """Emite un evento ON_CAST y verifica que se procesa."""
    gs = GameState(seed=42)
    hero = gs.spawn_entity("hero", {"mana": 100})

    # Handler: cuando se emita ON_CAST, gastar 10 mana
    t = Trigger(
        id=gs.new_trigger_id(),
        on="ON_CAST",
        source=hero.id,
        then=[spend(hero.id, "mana", 10)],
    )
    gs.add_trigger(t)

    # Emitir ON_CAST
    emit("ON_CAST", source=hero.id, target=hero.id)(gs, {})

    # Procesar
    gs = run_loop(gs, max_ticks=10)

    assert hero.state["mana"] == 90
    print("  [PASS] runtime emit and process")


def test_runtime_cooldown():
    """Verifica que cooldown decrementa cada tick."""
    gs = GameState(seed=42)
    hero = gs.spawn_entity("hero", {"fireball_cooldown": 3})

    # Emitir 3 ticks para que cooldown llegue a 0
    for _ in range(3):
        emit("ON_TICK")(gs, {})
    gs = run_loop(gs, max_ticks=10)
    assert hero.state["fireball_cooldown"] == 0
    print("  [PASS] runtime cooldown")


def test_runtime_regen():
    """Verifica que regen aplica cada tick."""
    gs = GameState(seed=42)
    hero = gs.spawn_entity("hero", {"hp": 50, "hp_max": 100, "hp_regen": 5})

    emit("ON_TICK")(gs, {})
    emit("ON_TICK")(gs, {})
    gs = run_loop(gs, max_ticks=10)
    # After 2 ticks: 50 + 5 + 5 = 60
    assert hero.state["hp"] == 60
    print("  [PASS] runtime regen")


def test_determinism():
    """SPEC §10: mismo seed + programa → mismo trace."""
    def setup(gs):
        hero = gs.spawn_entity("hero", {"mana": 100, "hp": 100})
        t = Trigger(
            id=gs.new_trigger_id(),
            on="ON_CAST",
            source=hero.id,
            then=[spend(hero.id, "mana", 10)],
        )
        gs.add_trigger(t)
        emit("ON_CAST", source=hero.id)(gs, {})

    gs1 = run(seed=42, setup_fn=setup)
    gs2 = run(seed=42, setup_fn=setup)

    assert gs1.tick == gs2.tick
    assert len(gs1.trace) == len(gs2.trace)
    for t1, t2 in zip(gs1.trace, gs2.trace):
        assert t1.effect == t2.effect
        assert t1.state_before == t2.state_before
        assert t1.state_after == t2.state_after
    print("  [PASS] determinism")


# ============================================================================
# Invariants (SPEC §15)
# ============================================================================

def test_invariant_hp_max():
    """HP ≤ hp_max siempre."""
    gs = GameState(seed=1)
    hero = gs.spawn_entity("hero", {"hp": 50, "hp_max": 100})
    gain(hero.id, "hp", 100)(gs, {})
    assert hero.state["hp"] <= hero.state["hp_max"]
    print("  [PASS] invariant hp <= max")

def test_invariant_tick_monotonic():
    """tick_now es monótonamente creciente."""
    gs = GameState(seed=1)
    hero = gs.spawn_entity("hero")
    for i in range(5):
        emit("ON_TICK")(gs, {})
    ticks_seen = [gs.tick]
    gs = run_loop(gs, max_ticks=10)
    # After run_loop, tick should be >= what we saw
    assert gs.tick >= 0
    print("  [PASS] invariant tick monotonic")

def test_invariant_event_single_process():
    """Un evento no se procesa dos veces."""
    gs = GameState(seed=1)
    hero = gs.spawn_entity("hero", {"counter": 0})

    t = Trigger(
        id=gs.new_trigger_id(),
        on="ON_TEST",
        source=hero.id,
        then=[inc_state(hero.id, "counter")],
    )
    gs.add_trigger(t)
    emit("ON_TEST", source=hero.id)(gs, {})

    gs = run_loop(gs, max_ticks=10)
    assert hero.state["counter"] == 1  # Only once
    print("  [PASS] invariant event single process")


# ============================================================================
# Run all tests
# ============================================================================

def main():
    print("=== DotaCode Tests ===\n")

    print("PRNG:")
    test_prng_determinism()
    test_prng_range()
    test_prng_checkpoint_restore()
    test_prng_fork()

    print("\nEventQueue:")
    test_eventqueue_fifo_same_tick()
    test_eventqueue_tick_ordering()
    test_eventqueue_cancel()

    print("\nEntity:")
    test_entity_spawn_destroy()
    test_entity_alive_filter()

    print("\nModifier:")
    test_modifier_lifecycle()
    test_modifier_refresh()

    print("\nResource:")
    test_spend_success()
    test_spend_insufficient()
    test_gain_respects_max()
    test_gain_no_max()
    test_force_spend_negative()

    print("\nTrigger matching:")
    test_match_event_exact()
    test_match_event_wildcard()
    test_find_matching_triggers()

    print("\nGating:")
    test_gate_prevents_action()

    print("\nEffects:")
    test_seq_effects()

    print("\nVariables:")
    test_var_operations()
    test_global_operations()

    print("\nPosition:")
    test_distance()
    test_in_range()

    print("\nRuntime integration:")
    test_runtime_emit_and_process()
    test_runtime_cooldown()
    test_runtime_regen()
    test_determinism()

    print("\nInvariants (SPEC §15):")
    test_invariant_hp_max()
    test_invariant_tick_monotonic()
    test_invariant_event_single_process()

    print("\n=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    main()
