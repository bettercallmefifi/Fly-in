"""Entry point for the Drone Routing Simulation program."""
import sys
from parsing import Parser, ParsingError
from simulation import Simulation
from visualizer import Visualizer


def valid_arg() -> str:
    """Parse command-line arguments to extract the map file."""
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Usage: python3 main.py <map_file>")
        sys.exit(1)


def main() -> None:
    """Execute the core logic: Parse map, calculate paths, run simulation."""
    file_name = valid_arg()
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

        # 7iyedna l'flag mn hna
        sim = Simulation(graph, parser.total_drones, best_paths)
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
