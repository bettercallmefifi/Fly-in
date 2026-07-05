from dataclasses import dataclass


@dataclass
class Connection:
    zone1_name: str
    zone2_name: str
    max_link_capacity: int