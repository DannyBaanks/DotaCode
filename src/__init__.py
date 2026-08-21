"""DotaCode — esolang experimental inspirado en Dota 2."""

try:
    from .prng import PRNG
    from .dtypes import Entity, Modifier, Event, Trigger, EventQueue, ActionType, Severity
    from .gamestate import GameState
    from .effects import *
    from .triggers import find_matching_triggers, match_event, eval_condition
    from .runtime import run, run_loop, process_event
except ImportError:
    from prng import PRNG
    from dtypes import Entity, Modifier, Event, Trigger, EventQueue, ActionType, Severity
    from gamestate import GameState
    from effects import *
    from triggers import find_matching_triggers, match_event, eval_condition
    from runtime import run, run_loop, process_event
