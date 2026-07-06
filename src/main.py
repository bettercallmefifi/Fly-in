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
        # 1. Kan-lanciou l'parsing howa lowel bach y3mer l'Graph
        parser.parsing()

        # 2. Kan-jebdou l'graph (bla a9was 7it attribut machi methode)
        graph = parser.graph

        # 3. N-printiw l'ma3loumat bach n-t2ekdou anaho kolchi dkhl mzyan
        print("================ Natija dyal l'Graph ================")
        print(f"Total Drones : {parser.total_drones}")
        print(f"Les Zones    : {len(graph.zones)}")
        print(f"Connections  : {len(graph.connections)}")
        print("=====================================================")

    except ParsingError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
