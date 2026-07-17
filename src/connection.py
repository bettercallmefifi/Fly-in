"""Module containing the Connection class logic."""


class Connection:
    """Represents a bidirectional edge connecting two zones."""

    def __init__(self, zone1: str, zone2: str, capacity: int):
        """Initialize the connection linking two zones with a max capacity."""
        self.zone1 = zone1
        self.zone2 = zone2
        self.capacity = capacity
        self.drones_on_link = 0
