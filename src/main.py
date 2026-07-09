import sys
from parsing import Parser, ParsingError

def valid_arg() -> str:
    if len(sys.argv) != 2:
        print("Invalid arguments")
        sys.exit(1)
    return sys.argv[1]


def main():
    file_name = valid_arg()
    parser = Parser(file_name)

    try:
        parser.parsing()

        graph = parser.graph

        print("\n================ Graph ========")
        print(f"Total Drones : {parser.total_drones}")
        print(f"Les Zones    : {len(graph.zones)}")
        print(f"Connections  : {len(graph.connections)}")
        print(f"Start Zone   : {graph.start_zone.name}")
        print(f"End Zone     : {graph.end_zone.name}")
        print("=======================================================")

        print("\n================ Natija dyal Pathfinding ==============")
        best_path = graph.calculate_drone_path()

        if best_path:
            # Kan-jbdou smyat dyal l'zones mn l'objects w kan-lasqohom b ' -> '
            path_names = [zone.name for zone in best_path]
            print(f"A9sar tri9 hiya: {' -> '.join(path_names)}")
            print(f"3adad l'Ma7attat f t-tri9: {len(best_path)}")
        else:
            print("Makaynach 7ta tri9 bin Start w End f had l'kharita!")
        print("=======================================================")

    except ParsingError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()