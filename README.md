*This project has been created as part of the 42 curriculum by feel-idr.*

# Fly-in: Drone Routing Simulation

## Description

Fly-in is an object-oriented Python simulation designed to route a fleet of autonomous drones from a starting hub to an end hub while minimizing the total number of simulation turns. The system reads a custom map file defining a graph of zones and connections, validates the input formatting, calculates optimized flight paths, and simulates turn-by-turn movements. The simulation strictly respects all constraints, including multi-turn travel for restricted zones and simultaneous drone capacity limits for hubs and connections.

## Algorithm Choices and Implementation Strategy

To achieve high efficiency and prevent bottlenecks, the project employs a custom pathfinding approach rather than sending all drones down a single shortest path:

* **Cost Evaluation:** A modified Dijkstra's algorithm evaluates paths based on zone types, assigning a cost of 1.0 for normal zones, 2.0 for restricted zones, 0.5 for priority zones, and infinite cost for blocked zones.


* **Traffic Distribution:** The system iterates through the graph, applying progressive penalties (`+0.01`) to heavily used zones. This forces the algorithm to discover multiple disjoint or overlapping paths, storing the combination that mathematically minimizes total turns for the specified number of drones.


* **Turn Mechanics:** During simulation, drones are sorted by their path progress. The engine checks `max_drones` and `max_link_capacity` before validating a move. If a drone enters a restricted zone, it is placed in a delayed state and physically occupies the connection until the next turn.



## Visual Representation

A graphical interface built with Pygame translates the turn-by-turn console output into a clear, interactive visualizer.

* **Dynamic Rendering:** The visualizer automatically scales the graph coordinates (`get_scaled_coords`) to fit seamlessly within the window, regardless of the map size.


* **Real-Time Data:** Zones display their names alongside live occupancy metrics (e.g., `[1/2]`), and connections dynamically change from blue to red and increase in thickness when they reach their maximum link capacity.


* **Interactive Interpolation:** Drone movements are smoothly animated between nodes. You can navigate through the simulation history manually using `->`, `SPACE`, or `ENTER` for the next turn, and `<-` or `BACKSPACE` for the previous turn.



## Instructions

The project is built using Python 3.10+ and relies on a `Makefile` to handle dependencies and execution.

**Setup:**

1. (Optional) Create a virtual environment:
```bash
make venv

```


2. Install the required dependencies (`pygame`, `flake8`, `mypy`):
```bash
make install

```



**Execution:**
Run the simulation with a specific map file (defaults to `map` if not specified):

```bash
make run MAP=<path_to_map_file>

```

**Development & Debugging Tools:**

* `make debug`: Runs the project using Python's built-in `pdb` debugger.


* `make clean`: Removes all `.pyc` files and cache directories (`__pycache__`, `.mypy_cache`, `cache`).


* `make lint`: Executes `flake8` and `mypy` with specific flags (`--warn-return-any`, `--check-untyped-defs`, etc.) to enforce strict type safety and code quality.


* `make lint-strict`: Runs the strictest possible linting checks.



## Resources

* [Pygame Documentation](https://www.pygame.org/docs/) - Referenced for rendering the graphical interface, drawing lines/circles, and handling user key-press events.
* [Python heapq Module](https://docs.python.org/3/library/heapq.html) - Utilized for the priority queue implementation within the Dijkstra pathfinding algorithm.
* **AI Usage Description:** AI was used to assist in brainstorming the math for dynamically scaling screen coordinates in the Pygame visualizer.