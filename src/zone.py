from drone import Drone
from typing import List


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        max_drones: int = 1,
        color: str = "none",
        zone_type: str = "normal",
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.max_drones = max_drones
        self.zone_type = zone_type
        self.color = color

        self.current_drones_inside = 0
        self.drones: List[Drone] = []
        self.neighbors: List[Zone] = []
