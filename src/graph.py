from pathfinding import Pathfinding


class Graph:
    def __init__(self):
        self.zones = {}
        self.connections = []
        self.start_zone = None
        self.end_zone = None
        self.adjacency_list = {}

    def add_zone(self, zone):
        self.zones[zone.name] = zone
        self.adjacency_list[zone] = []

    def add_connection(self, connection):
        self.connections.append(connection)

        z1 = self.zones[connection.zone1]
        z2 = self.zones[connection.zone2]
        self.adjacency_list[z1].append(z2)
        self.adjacency_list[z2].append(z1)

    def calculate_drone_path(self, total_drones):
        if not self.start_zone or not self.end_zone:
            return None

        finder = Pathfinding()

        best_paths = finder.find_smart_paths(
            self.start_zone,
            self.end_zone,
            self.adjacency_list,
            total_drones
        )

        return best_paths
