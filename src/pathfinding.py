import heapq
from typing import Dict, List, Optional, Any


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

    def find_shortest_path(self,
        start_zone: Any,
        end_zone: Any,
        adjacency_list: Dict[Any, List[Any]]
    ) -> Optional[List[Any]]:

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

                cost = self.get_zone_cost(neighbor.zone_type)

                if cost == float('inf'):
                    continue

                new_cost = current_cost + cost
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous_nodes[neighbor] = current_zone
                    heapq.heappush(pq, (new_cost, neighbor.name, neighbor))
        return None

    def build_path(self,
                previous_nodes: Dict[Any, Any],
                end_zone: Any
                )-> List[Any]:
        path = []
        current = end_zone
        while current is not None:
            path.append(current)
            current = previous_nodes.get(current)
		
        path.reverse()
        return path