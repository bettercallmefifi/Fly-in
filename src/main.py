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

        # f weste def main(), wste bloc try:
        print("\n================ Natija dyal Pathfinding ==============")
        # Kan-passiw total_drones l'graph
        best_paths = graph.calculate_drone_path(parser.total_drones)

        if best_paths:
            print(f"L9ina {len(best_paths)} tor9an ma-kayt9at3ouch!")
            for i, path in enumerate(best_paths, 1):
                path_names = [zone.name for zone in path]
                print(f"Tri9 {i}: {' -> '.join(path_names)} (Toul: {len(path)-1})")
        else:
            print("Makaynach 7ta tri9 bin Start w End f had l'kharita!")
        print("=======================================================")

    except ParsingError as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
'''import sys
from parsing import Parser, ParsingError

def main():
    # 1. Kan-t2akdou blli dkhlna smyat l-fichier
    #  f command line (mthal: make run MAP=...)
    if len(sys.argv) < 2:
        print("❌ Error: Khassk t-3ti smyat l-fichier dyal l-map!")
        print("Mthal: python3 src/main.py maps/easy/01_linear_path.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    try:
        # 2. Kan-kreyiw l'Parser w kan-lanciwh
        parser = Parser(file_name)
        parser.parsing()

        # Ila wselna hna, ya3ni l-parsing daz b naja7 bla machakil
        print(f"✅ Parsing daz mzyan l-fichier: {file_name}")
        print(f"🚁 Total Drones: {parser.total_drones}")
        print("=" * 60)

        # 3. N-printiw ZONES
        print("\n📍 ZONES L-MAWJOUDIN:")

        # Kan-ftardou blli 'parser.graph.zones'
        # fiha l-ma7attat (Dictionary wla List)
        # Ila kant Dictionary {smiya: Zone_Object}, 3yyt liha b .values():
        if hasattr(parser.graph, 'zones'):
            # Check ila kant dict wla list
            zones_list = parser.graph.zones.values()
            if isinstance(parser.graph.zones, dict) else parser.graph.zones

            for z in zones_list:
                print(f" - M7tta: [{z.name}]
                | X:{z.x} Y:{z.y} | Max Drones:
                 {z.max_drones} | Color: {z.color} |
                 Type: {z.zone_type}")
        else:
            print(" ⚠️ L-Classe Graph dyalek ma-fihach l-attribut 'zones'.")

        print("\n" + "=" * 60)

        # 4. N-printiw CONNECTIONS
        print("\n🔗 CONNECTIONS (T-TORQAN):")

        if hasattr(parser.graph, 'connections'):
            for c in parser.graph.connections:
                # Kan-ftardou blli l-Connection 3ndha name1, name2 w l-capacity
                # Ila knti msmihom f
                #  l-classe Connection b smia khra
                # (mthal: c.zone1 w c.zone2), beddelhom hna
                n1 = getattr(c, 'name1', getattr(c, 'zone1', 'Unknown'))
                n2 = getattr(c, 'name2', getattr(c, 'zone2',
                 'Unknown'))
                cap = getattr(c, 'data',
                getattr(c, 'capacity', getattr(c, 'max_link_capacity', 1)))

                print(
                f" - Triq bin: [{n1}] <---> [{n2}] | Max Capacity: {cap}"
                )
        else:
            print(
            " ⚠️ L-Classe Graph dyalek ma-fihach l-attribut 'connections'."
            )

        print("\n" + "=" * 60)

    except ParsingError as e:
        # Ila lqa chi mouchkil f l-parsing
        # (b7al Metadata empty), ghadi y-tbe3 lik l-error hna
        print(f"❌ Error f l'Parsing:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()'''
