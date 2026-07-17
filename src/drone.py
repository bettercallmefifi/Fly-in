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
