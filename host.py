#!/usr/bin/env python3
"""
DotaCode Host — motor público genérico, todo en uno.

Ejecuta programas DotaCode (API Python) y ejemplos del corpus.
No expone infraestructura interna, solo el runtime público.

Uso:
  py host.py --list
  py host.py corpus/01_kill_counter.py
  py host.py examples/examples_10.py
  py host.py --all
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reusa el runtime público
ROOT = Path(__file__).parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from runtime import run, run_loop
from gamestate import GameState


def list_corpus() -> None:
    print("DotaCode — corpus canónico")
    print("=" * 60)
    corpus = sorted((ROOT / "corpus").glob("*.py")) if (ROOT / "corpus").exists() else []
    for p in corpus:
        print(f"{p.name:30s} # {p.read_text(encoding='utf-8').splitlines()[0][:50]}")
    print(f"\nTotal: {len(corpus)}")
    print("\nPrimitivas (7): Entity, State, Event, Effect, Trigger, Modifier, Time")
    print("Ejemplos megacompose: 10")


def run_file(path: Path) -> int:
    # Cada archivo corpus define setup(gs) o main()
    code = path.read_text(encoding="utf-8")
    # Ejecuta el archivo como módulo que define setup
    ns: dict = {}
    try:
        exec(compile(code, str(path), "exec"), ns)
    except Exception as e:
        print(f"Error cargando {path.name}: {e}", file=sys.stderr)
        return 2

    # Busca setup o main o example_*
    setup = ns.get("setup")
    if setup is None:
        # busca primer def example_* o test_*
        for k, v in ns.items():
            if k.startswith("example_") or k.startswith("setup"):
                if callable(v):
                    setup = v
                    break
    if setup is None and "main" in ns and callable(ns["main"]):
        try:
            ns["main"]()
            return 0
        except Exception as e:
            print(f"Error en main {path.name}: {e}", file=sys.stderr)
            return 3

    if setup is None:
        print(f"{path.name}: no se encontró setup(gs) ni main()", file=sys.stderr)
        return 2

    try:
        gs = run(seed=42, setup_fn=setup)
    except Exception as e:
        print(f"Error ejecutando {path.name}: {e}", file=sys.stderr)
        return 3

    # Estado final mínimo
    print(f"--- {path.name} ---")
    print(f"tick={gs.tick} events_pending={gs.events.qsize() if hasattr(gs.events, 'qsize') else 'n/a'}")
    for e in gs.alive_entities():
        print(f"  {e.type}#{e.id} state={e.state} alive={e.alive}")
    if gs.output:
        print(f"  output={gs.output[:5]}")
    return 0


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="DotaCode Host — ejecuta corpus")
    p.add_argument("file", nargs="?", help="Archivo .py del corpus o ejemplo")
    p.add_argument("--list", action="store_true", help="Lista corpus")
    p.add_argument("--all", action="store_true", help="Ejecuta todo el corpus")

    args = p.parse_args()

    if args.list:
        list_corpus()
        return

    if args.all:
        corpus = sorted((ROOT / "corpus").glob("*.py"))
        if not corpus:
            print("corpus vacío, ejecuta gen_17_dota.py primero", file=sys.stderr)
            sys.exit(2)
        fails = 0
        for f in corpus:
            code = run_file(f)
            if code != 0:
                fails += 1
        print(f"\nCorpus: {len(corpus)-fails}/{len(corpus)} OK")
        sys.exit(1 if fails else 0)

    if args.file:
        sys.exit(run_file(Path(args.file)))

    p.print_help()


if __name__ == "__main__":
    main()
