# *This project has been created as part of the 42 curriculum by feel-idr.*

## Description

**Fly-in** is a simulation project designed to manage a fleet of autonomous drones navigating a network of connected zones. The core objective is to route all drones from a designated `start_hub` to a `goal_hub` in the fewest possible turns, while respecting strict zone occupancy rules, connection capacities, and movement costs associated with different zone types (normal, restricted, priority, blocked).

## Instructions

### Installation

To set up the project, ensure you have Python 3.10+ installed. Create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
make install

```

### Execution

You can run the simulation by passing a map file to the main script:

```bash
# Basic run
make run MAP=maps/easy/01_linear_path.txt

# Run with capacity info flag
python3 src/main.py --capacity-info maps/easy/01_linear_path.txt

```

### Cleanup

To remove temporary files and caches:

```bash
make clean

```

## Implementation Strategy

The solution employs a **Dijkstra-based pathfinding algorithm** to dynamically determine the most efficient routes.

* **Path Planning**: We calculate a weighted shortest path from the start to the end, applying penalties to zones to distribute drone traffic and prevent congestion.


* **Turn Scheduling**: The simulation engine operates turn-by-turn. It evaluates zone and connection capacities in real-time. Drones destined for `restricted` zones are scheduled with a 2-turn movement cost, where the destination capacity is reserved immediately to prevent deadlocks.


* **Animation**: The visualizer uses linear interpolation between nodes to provide a smooth graphical representation of drone movement, while allowing the user to navigate the simulation history using arrow keys.



## Visual Representation

The project features two modes of feedback:

1. **Graphical Interface**: A `pygame`-based window that displays the graph layout, current occupancy of zones (`current/max`), and real-time movement of drones with interpolation.


2. **Terminal Output**: A step-by-step log in the standard format `D<ID>-<zone>`, providing a clear history of all drone movements throughout the simulation.



## Resources

* **Documentation**: Official Python documentation for `typing`, `heapq`, and `pygame`.
* **AI Usage**: AI tools were utilized to assist with the structure of the simulation loop, debugging `mypy` type-checking errors, and implementing the `pygame` interpolation logic. All generated code was reviewed, tested, and integrated by the developer to ensure full understanding.

---
