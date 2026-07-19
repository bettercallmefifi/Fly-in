"""Module containing the Drone class logic."""
from typing import List, Optional, Any


class Drone:
    """Represents an autonomous drone navigating the network."""

    def __init__(self, drone_id: str, path: List[Any]):
        """Initialize the drone with an ID and a designated path."""
        self.id = drone_id
        self.path = path
        self.current_step = 0
        self.status = "waiting"

    def get_current_zone(self) -> Optional[Any]:
        """Return the zone the drone is currently occupying."""
        if self.current_step < len(self.path):
            return self.path[self.current_step]
        return None

    def get_next_zone(self) -> Optional[Any]:
        """Return the next zone in the drone's path."""
        if self.current_step + 1 < len(self.path):
            return self.path[self.current_step + 1]
        return None

    def move(self) -> None:
        """Advance the drone to the next step in its path."""
        if self.status != "arrived" and self.get_next_zone() is not None:
            self.current_step += 1
            self.status = "moving"

            if self.current_step == len(self.path) - 1:
                self.status = "arrived"


def initialize_drones(
        total_drones: int,
        best_paths: List[List[Any]]
) -> List[Drone]:
    """Instantiate Drone objects and assign them their calculated paths."""
    drones_list = []
    path_index = 0

    for i in range(1, total_drones + 1):
        drone_id = f"D{i}"
        chosen_path = best_paths[path_index % len(best_paths)]
        new_drone = Drone(drone_id, chosen_path)
        drones_list.append(new_drone)
        path_index += 1

    return drones_list
