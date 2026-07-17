import sys
from parsing import Parser, ParsingError
from simulation import Simulation
from visualizer import Visualizer


def valid_arg() -> str:
    if len(sys.argv) != 2:
        print("Invalid arguments")
        sys.exit(1)
    return sys.argv[1]


def main() -> None:
    file_name = valid_arg()
    parser = Parser(file_name)

    try:
        parser.parsing()
        graph = parser.graph

        if not graph.start_zone or not graph.end_zone:
            print("Start Zone or End Zone missing in the graph!")
            return

        print("\n================ Graph ========")
        print(f"Total Drones : {parser.total_drones}")
        print(f"Les Zones    : {len(graph.zones)}")
        print(f"Connections  : {len(graph.connections)}")
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("=======================================================")

        best_paths = graph.calculate_drone_path(parser.total_drones)

        if not best_paths:
            print("Makaynach 7ta tri9 bin Start w End f had l'kharita!")
            return

        sim = Simulation(graph, parser.total_drones, best_paths)
        vis = Visualizer()

        sim.run(visualizer=vis)

        while True:
            vis.handle_events()

    except ParsingError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
