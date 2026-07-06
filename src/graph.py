from zone import Zone
from connection import Connection
from drone import Drone
from typing import Dict, List


class Graph:
	def __init__(self):
		self.nb_drones = 0
		self.zones: Dict[str, Zone] = {}
		self.start_zone: Zone | None = None
		self.end_zone: Zone | None = None
		self.connections: List[Connection] = []
		self.drones: List[Drone] = []

	def add_zone(self, new_zone: Zone):
		self.zones[new_zone.name] = new_zone
	
	def add_connection(self, new_connection: Connection):
		self.connections.append(new_connection)
