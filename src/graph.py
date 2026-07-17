"""Module containing the Graph class for representing the drone network."""
from pathfinding import Pathfinding
from typing import Dict, List, Optional, Any, Tuple


class Graph:
    """Represents the network of zones and
    connections for drone routing."""

    def __init__(self) -> None:
        """Initialize an empty graph with zones,
        connections, and adjacencies."""
        self.zones: Dict[str, Any] = {}
        self.connections: List[Any] = []
        self.start_zone: Optional[Any] = None
        self.end_zone: Optional[Any] = None
        self.adjacency_list: Dict[Any, List[Any]] = {}
        self.connection_map: Dict[Tuple[str, str], Any] = {}

    def add_zone(self, zone: Any) -> None:
        """Add a new zone to the graph and initialize its adjacency list."""
        self.zones[zone.name] = zone
        self.adjacency_list[zone] = []

    def add_connection(self, connection: Any) -> None:
        """Add a bidirectional connection between two zones in the graph."""
        self.connections.append(connection)
        z1 = self.zones[connection.zone1]
        z2 = self.zones[connection.zone2]

        self.adjacency_list[z1].append(z2)
        self.adjacency_list[z2].append(z1)

        self.connection_map[(z1.name, z2.name)] = connection
        self.connection_map[(z2.name, z1.name)] = connection

    def get_connection(self, zone_name1: str, zone_name2: str) -> Any:
        """Retrieve the connection object linking two specific zone names."""
        return self.connection_map.get((zone_name1, zone_name2))

    def calculate_drone_path(
            self,
            total_drones: int
    ) -> Optional[List[List[Any]]]:
        """Calculate and return the optimized paths for all drones."""
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
