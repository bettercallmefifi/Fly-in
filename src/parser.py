from graph import Graph
from typing import Dict
from zone import Zone


class ParssingError(Exception):
	pass

class Parser:
	def __init__(self, filename: str) -> None:
		self.filename = filename
		self.graph = Graph()

	def parse(self) -> Graph:
		try:
			with open(self.filename, "r") as f:
				lines = f.readlines()
		except FileNotFoundError:
			raise ParssingError(f"File not found '{self.filename}'")
		
		exist = False

		for line in lines:
			line = line.strip()

			if not line or line.startswith("#"):
				continue
				
			if line.startswith("nb_drones:"):
				if exist:
					raise ParssingError("nb_drones already defined !")
				self.parse_nb_drones(line)
				exist = True
			
			elif line.startswith("start_hub:"):
				self.parse_start_zone(line)
			
			elif line.startswith("end_hub"):
				self.parse_end_zone(line)
			
			elif line.startswith("hub:"):
				self.parse_zone(line)
			
			elif line.startswith("connection:"):
				self.parse_connection(line)
			else:
				raise ParssingError(f"Invalid line detected ! {line}")
		
		if not self.graph.end_zone:
			raise ParssingError("No end zone detected !")
		if not self.graph.start_zone:
			raise ParssingError("No start zone detected !")
		if not exist:
			raise ParssingError("There is no Drone detected !")
		return self.graph
	
	def parse_nb_drones(self, line: str) -> None:
		content = line.replace(
			"nb_drones:",
			"",
		).strip()
		n = int(content)
		if n <= 0:
			raise ParssingError(f"Invalid number {n} o drones")
		self.graph.nb_drones = n
	
	def parse_attributes(
			self,
			attributes_str: str,
	) -> Dict[str, str]:
		attributes: Dict[str, str] = {}

		attributes_str = (
			attributes_str
			.replace("[", "")
			.replace("]", "")
			.strip()
		)
		if not attributes_str:
			return attributes
		
		for item in attributes_str.split():

			if "=" not in item:
				raise ParssingError(f"Invalid metadata: {item}")
			elements = item.split("=")
			if not len(elements) == 2:
				raise ParssingError("Invalid item:", item)
			key, value = elements
			if not key or not value:
				raise ParssingError(f"Invalid metedata: {item}")
			
			attributes[key] = value
		
		return attributes
	
	def build_zone(
			self,
			contend: str,
			start_or_end: bool = False
	) -> Zone:
		if "[" in contend:
			zone_part = content[
				:contend.index("[")
			].strip()

			attributes_part = contend[
				contend.index("["):
			]
		else:
			zone_part = contend
			attributes_part = ""

		parts = zone_part.split
		if len(parts) < 3:
			raise ParssingError("Name and Coordonates are required 1 !")
		if len (parts) > 3:
			raise ParssingError("Not required infos detected !")
		name = parts[0]
		try:
			x = int(parts[1])
			y = int(parts[2])
		except ValueError:
			raise ParssingError("Only numbers are valid as a coordinates !")
		
		attributes = self.parse_attributes(attributes_part)

		for a in attributes.keys():
			if a not in ["zone", "color", "max_drones"]:
				raise ParssingError(f"Invalid metadata: {a}")
		zone_type = attributes.get(
			"zone",
			"normale"
		)

		color = attributes.get(
			"color",
			"none"
		)

		try:
			if start_or_end:
				max_drones = self.graph.nb_drones
			else:
				max_drones = int(
					attributes.get(
						"max_drones",
						1
					)
				)
		except ValueError:
			raise ParssingError("Only Numbers accepted !")
		if max_drones < 0:
			raise ParssingError("zone capacity cannot be negative !")
		
		try:
			zone = Zone(
				name=name,
				x=x,
				y=y,
				zone_type=zone_type,
				color=color,
				max_drones=max_drones,
			)
		except ValueError as e:
			raise ParssingError(e)