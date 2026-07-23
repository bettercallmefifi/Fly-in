"""Entry point for the Drone Routing Simulation program."""
import sys
from parsing import Parser, ParsingError
from simulation import Simulation
from visualizer import Visualizer
from typing import Tuple


def valid_arg() -> Tuple[str, bool]:
    """Parse command-line arguments to extract the map file."""
    if len(sys.argv) == 3 and sys.argv[1] == "--capacity-info":
        return sys.argv[2], True
    elif len(sys.argv) == 2:
        return sys.argv[1], False
    else:
        print("Usage: python3 main.py --capacity-info <map_file>")
        sys.exit(1)


def main() -> None:
    """Execute the core logic: Parse map, calculate paths, run simulation."""
    file_name, flag = valid_arg()
    parser = Parser(file_name)

    try:
        parser.parsing()
        graph = parser.graph

        if not graph.start_zone or not graph.end_zone:
            print("Start Zone or End Zone missing in the graph!")
            return

        print("\n====================== Graph ==========================")
        print(f"Total Drones : {parser.total_drones}")
        print(f"Les Zones    : {len(graph.zones)}")
        print(f"Connections  : {len(graph.connections)}")
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("=======================================================")

        best_paths = graph.calculate_drone_path(parser.total_drones)

        if not best_paths:
            print("There is no path from the start to the end zone!")
            return

        sim = Simulation(graph, parser.total_drones, best_paths, flag)
        sim.run()

        vis = Visualizer()
        vis.run(sim)

    except ParsingError as e:
        print(f"{e}")

    except KeyboardInterrupt:
        print("\nSimulation interrupted by user. Exiting cleanly...")
        sys.exit(0)


if __name__ == "__main__":
    main()
