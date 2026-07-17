"""Module containing the Pathfinding algorithm logic."""
import heapq
from typing import Dict, List, Optional, Any


class Pathfinding:
    """Handles the pathfinding logic to route drones efficiently."""

    def __init__(self) -> None:
        """Initialize the Pathfinding object."""
        pass

    def get_zone_cost(self, zone_type: str) -> float:
        """Determine the movement cost based on the zone type."""
        if zone_type == "blocked":
            return float('inf')
        elif zone_type == "restricted":
            return 2.0
        elif zone_type == "priority":
            return 0.5
        else:
            return 1.0

    def find_shortest_path(
        self,
        start_zone: Any,
        end_zone: Any,
        adjacency_list: Dict[Any, List[Any]],
        zone_penalties: Optional[Dict[Any, float]] = None
    ) -> Optional[List[Any]]:
        """Find the shortest path between start
        and end zones using Dijkstra."""
        if zone_penalties is None:
            zone_penalties = {}

        distances = {start_zone: 0.0}
        previous_nodes = {start_zone: None}

        pq = [(0.0, start_zone.name, start_zone)]
        visited = set()

        while pq:
            current_cost, _, current_zone = heapq.heappop(pq)

            if current_zone == end_zone:
                return self.build_path(previous_nodes, end_zone)

            if current_zone in visited:
                continue

            visited.add(current_zone)
            neighbors = adjacency_list.get(current_zone, [])

            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                base_cost = self.get_zone_cost(neighbor.zone_type)

                if base_cost == float('inf'):
                    continue

                penalty = zone_penalties.get(neighbor, 0.0)
                cost = base_cost + penalty

                new_cost = current_cost + cost
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous_nodes[neighbor] = current_zone
                    heapq.heappush(pq, (new_cost, neighbor.name, neighbor))
        return None

    def build_path(
        self,
        previous_nodes: Dict[Any, Any],
        end_zone: Any
    ) -> List[Any]:
        """Reconstruct the path from the end zone back to the start zone."""
        path = []
        current = end_zone
        while current is not None:
            path.append(current)
            current = previous_nodes.get(current)

        path.reverse()
        return path

    def find_smart_paths(
        self,
        start_zone: Any,
        end_zone: Any,
        adjacency_list: Dict[Any, List[Any]],
        total_drones: int
    ) -> List[List[Any]]:
        """Find a combination of paths to minimize total simulation turns."""
        all_unique_paths: List[List[Any]] = []
        zone_penalties: Dict[Any, float] = {}
        best_turn_count: float = float('inf')
        best_paths_combination: List[List[Any]] = []

        for _ in range(50):
            new_path = self.find_shortest_path(
                start_zone,
                end_zone,
                adjacency_list,
                zone_penalties
            )
            if not new_path:
                break

            for zone in new_path:
                if zone != start_zone and zone != end_zone:
                    zone_penalties[zone] = zone_penalties.get(zone, 0.0) + 0.01

            if new_path not in all_unique_paths:
                all_unique_paths.append(new_path)
                current_turns = self.calculate_turns(
                    all_unique_paths, total_drones
                    )

                if current_turns < best_turn_count:
                    best_turn_count = current_turns
                    best_paths_combination = list(all_unique_paths)

        return (best_paths_combination if
                best_paths_combination else all_unique_paths)

    def calculate_turns(
            self,
            paths: List[List[Any]],
            total_drones: int
    ) -> float:
        """Estimate the total number of turns required for the given paths."""
        if not paths:
            return float('inf')

        path_lengths = [len(p) - 1 for p in paths]
        path_lengths.sort()

        shortest_len = path_lengths[0]
        k = len(path_lengths)

        diff_sum = sum(length - shortest_len for length in path_lengths)

        if total_drones > diff_sum:
            drones_left = total_drones - diff_sum
            turns = shortest_len - 1 + diff_sum + (drones_left + k - 1) // k
            return float(turns)
        else:
            return float(shortest_len - 1 + total_drones)
