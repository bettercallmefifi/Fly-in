from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from drone import Drone


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: str = "normal",
        color: str = "none",
        max_drones: int = 1,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y

        self.zone_type = zone_type
        self.color = color

        self.max_drones = max_drones

        self.pending_drones: int = 0

        self.current_drones: int = 0

        self.drones: List[Drone] = []

        self.reserved_spot: int = 0

        self.neighbors: List[Zone] = []
        if self.zone_type not in [
            "normal",
            "restricted",
            "blocked",
            "priority",
        ]:
            raise ValueError("invalid zone type detected")

        if "-" in self.name:
            raise ValueError(
                "dashes are not allowed in zones name: ",
                self.name
                )

    def movement_cost(self) -> int:
        """calculate the mvt cost based on the zone type"""

        if self.zone_type == "restricted":
            return 2

        if self.zone_type in ("normal", "priority"):
            return 1

        raise ValueError(f"Blocked zone: {self.name}")

    def is_blocked(self) -> bool:
        """check if the zone is blocked"""
        return self.zone_type == "blocked"

    def can_accept_drone(self) -> bool:
        """"check if the drone can accept a drone"""
        return self.current_drones < self.max_drones

    def add_neighbor(self, neighbor: Zone) -> None:
        """add  a neighbor to the zone"""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def enter(self, d: Drone) -> None:
        """add a drone to the zone"""
        if self.current_drones < self.max_drones:
            self.current_drones += 1
            self.drones.append(d)
        else:
            raise ValueError("cannot add drones !")

    def leave(self, d: Drone) -> None:
        """remove a drone from the zone"""
        if self.current_drones > 0:
            self.current_drones -= 1
            self.drones.remove(d)
