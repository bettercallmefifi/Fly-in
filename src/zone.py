from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class ZoneType(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"
    PRIORITY = "priority"


@dataclass
class Zone:
    name: str
    zone_type: ZoneType
    max_drones: int
    x: int
    y: int
    color: Optional[str] = None
