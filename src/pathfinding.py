import heapq
from typing import Dict, List, Optional, Any, Set


class Pathfinding:
    def __init__(self):
        pass

    def get_zone_cost(self, zone_type: str) -> float:
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
        blocked_zones: Set[Any] = None
    ) -> Optional[List[Any]]:

        if blocked_zones is None:
            blocked_zones = set()

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

                if neighbor in blocked_zones and neighbor != end_zone:
                    continue

                if neighbor in visited:
                    continue

                cost = self.get_zone_cost(neighbor.zone_type)

                if cost == float('inf'):
                    continue

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
        path = []
        current = end_zone
        while current is not None:
            path.append(current)
            current = previous_nodes.get(current)

        path.reverse()
        return path

    def find_disjoint_paths(
            self,
            start_zone: Any,
            end_zone: Any,
            adjacency_list: Dict[Any, List[Any]],
            total_drones: int
    ) -> List[List[Any]]:

        all_path = []
        blocked_zones = set()
        best_turn_count = float('inf')
        best_paths_combination = []

        while True:
            new_path = self.find_shortest_path(
                start_zone,
                end_zone,
                adjacency_list,
                blocked_zones
            )

            if not new_path:
                break

            all_path.append(new_path)

            for zone in new_path:
                if zone != start_zone and zone != end_zone:
                    blocked_zones.add(zone)
            current_turns = self.calculate_turns(all_path, total_drones)

            if current_turns >= best_turn_count:
                all_path.pop()
                break
            else:
                best_turn_count = current_turns
                best_paths_combination = list(all_path)

        return best_paths_combination

    def calculate_turns(
            self,
            paths: List[List[Any]],
            total_drones: int
    ) -> int:

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
            return turns
        else:
            return shortest_len - 1 + total_drones
