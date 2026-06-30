# Fly-In

Fly-In is a 42 curriculum algorithm project about routing multiple drones through a graph of zones while respecting movement costs, zone capacities, link limits, and turn-by-turn simulation rules.

This README is a working roadmap for the project. It summarizes the subject, the implementation plan, and the tasks that still need to be completed to reach a fully reviewable submission.

## Project Goal

Build a Python 3.10+ application that:

- parses the custom map format used by the subject,
- computes valid and efficient paths for all drones,
- simulates their movement turn by turn without collisions,
- prints the moves for each simulation turn,
- provides a visual or colored representation of the run,
- passes `flake8` and `mypy` without errors,
- ships with the required `Makefile` commands.

The main optimization target is to finish the simulation in the fewest possible turns while keeping the solution correct on every map category.

## Subject Rules To Respect

- Python 3.10 or later.
- Object-oriented design.
- No external graph libraries such as `networkx` or `graphlib`.
- Type hints everywhere they matter.
- Strict `flake8` compliance.
- `mypy` must pass cleanly.
- Graceful error handling for invalid input files.
- Required `Makefile` targets: `install`, `run`, `debug`, `clean`, `lint`.
- Output must show the drones moved on each turn.

## Current Repository Layout

- `src/parser.py` handles input parsing.
- `src/zone.py` contains the zone model.
- `src/main.py` currently drives the menu / entry point flow.
- `src/graph.py`, `src/bfs.py`, `src/drone.py`, `src/connection.py`, `src/paths_manager.py`, `src/simulator.py`, and `src/visualisation.py` are the main implementation surfaces still to be completed or stabilized.
- `maps/` contains the evaluation maps grouped by difficulty.

## Roadmap

### Phase 1: Define the foundation

Goal: lock the project structure and the core data model before writing the optimization logic.

Tasks:

- confirm the final module responsibilities for parser, graph, simulation, and visualization,
- normalize the naming of entities such as zones, connections, drones, and hubs,
- define the public APIs shared between modules,
- add docstrings and type hints to every public class and function,
- create the `Makefile` and the development commands required by the subject.

### Phase 2: Finish the parser

Goal: reliably read the map format and reject malformed inputs with clear errors.

Tasks:

- parse drone count metadata,
- parse start and end hubs,
- parse normal, restricted, priority, and blocked zones,
- parse zone metadata such as color and capacity,
- parse connections between zones,
- validate duplicate definitions and missing required fields,
- validate numeric fields and zone constraints,
- raise subject-friendly parsing errors instead of crashing.

### Phase 3: Build the graph model

Goal: represent the map in memory in a way that supports pathfinding and simulation.

Tasks:

- store zones as nodes and connections as edges,
- track neighbors and capacities,
- store movement cost per zone type,
- expose helpers to check blocked zones and available capacity,
- keep the start and end hubs as special cases with infinite practical throughput.

### Phase 4: Implement pathfinding

Goal: compute usable routes that minimize total turns and avoid dead ends, loops, and bottlenecks.

Tasks:

- implement a shortest-path strategy suitable for weighted movement costs,
- account for restricted zones that cost 2 turns,
- prefer priority zones when multiple valid routes exist,
- avoid blocked zones completely,
- detect and handle dead ends and cycles,
- prepare path sets for multiple drones, not just a single route,
- support capacity-aware routing when a shorter path is not actually usable.

### Phase 5: Add turn-based simulation

Goal: move drones step by step while respecting all occupancy rules.

Tasks:

- simulate all drones across turns,
- ensure no zone exceeds `max_drones`,
- ensure no link or connection capacity is exceeded,
- handle waiting when a drone cannot move safely,
- resolve conflicts deterministically,
- stop the simulation when all drones reach the end hub.

### Phase 6: Produce the required output

Goal: show the simulation in the exact format expected by the subject.

Tasks:

- print each turn as a line of drone movements,
- keep the format stable and machine-readable,
- make sure the final run is easy to compare against expected output,
- add helpful summaries or debug logs only outside the strict output path.

### Phase 7: Add visualization

Goal: give the user a readable view of the simulation.

Tasks:

- implement a terminal-based colored view or a graphical interface,
- display zones, traffic, and drone progress clearly,
- keep the visual layer separate from core simulation logic,
- make the visual mode optional so it does not interfere with evaluation output.

### Phase 8: Validate and harden

Goal: make the project review-ready.

Tasks:

- run the project against all easy maps first,
- then validate medium and hard maps,
- measure turn counts and adjust heuristics where needed,
- run `flake8` and `mypy` regularly,
- add focused tests for parser failures and routing edge cases,
- confirm the Makefile commands work on a clean environment.

## Suggested Task Checklist

- [ ] Finalize the parser and error handling.
- [ ] Implement the graph and connection model.
- [ ] Implement the drone model.
- [ ] Implement pathfinding for weighted zones.
- [ ] Add capacity-aware scheduling.
- [ ] Build the simulation engine.
- [ ] Print turn-by-turn movements.
- [ ] Add visualization.
- [ ] Add tests for valid and invalid maps.
- [ ] Add `Makefile` targets.
- [ ] Fix lint and typing issues.
- [ ] Verify all map tiers.

## Recommended Build Order

1. Parser and data model.
2. Graph construction and validation.
3. Shortest-path logic.
4. Simulation engine and conflict resolution.
5. Output format and visualization.
6. Testing, linting, and typing cleanup.

## Definition Of Done

The project is ready when:

- every provided map can be parsed,
- the simulation produces valid moves for every turn,
- drones never violate capacity or occupancy rules,
- the output is stable and compliant with the subject,
- `make run`, `make debug`, `make lint`, `make clean`, and `make install` work,
- `flake8` and `mypy` complete successfully,
- the README documents the roadmap and the implementation status clearly.

## Notes For Future Work

- If the solver struggles on hard maps, the next improvement should be better scheduling rather than changing the parser.
- If the parser accepts bad input, fix validation before tuning the algorithm.
- If the output format is inconsistent, correct that before adding new features.
- If the visual layer slows down the solver, keep it optional and decoupled.
