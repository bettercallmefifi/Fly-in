class ParsingError(Exception):
	pass

class Parser:
	def __init__(self, file_name: str):
		self.file_name = file_name

	def parsing(self):
		try:
			with open(self.file_name, "r") as f:
				lines = f.readlines()
		except FileNotFoundError:
			raise ParsingError("Choose an existing file !")
		nb_drone_exist = False
		end_zone_exist = False
		start_zone_exist = False

		for line in lines:
			line = line.strip().lower()
			if not line or line.startswith("#"):
				continue

			elif line.startswith("nb_drones:"):
				if nb_drone_exist:
					raise ParsingError("nb_drones already exist !")
				self.parse_nb_drones(line)
				nb_drone_exist = True

			elif line.startswith("start_hub:"):
				if start_zone_exist:
					raise ParsingError("start_hub already exist !")
				self.parse_start_zone(line)
				start_zone_exist = True

			elif line.startswith("end_hub:"):
				if end_zone_exist:
					raise ParsingError("end_hub already exist !")
				self.parse_end_zone(line)
				end_zone_exist = True

			elif line.startswith("hub:"):
				self.parse_zone(line)

			elif line.startswith("connection:"):
				self.parse_connection(line)
			else:
				raise ParsingError("There is no data !")

	def parse_nb_drones(self, line: str) -> None:
		line = line.split(": ")
		if len(line) != 2:
			raise ParsingError("Invalid data !")
		try:
			nb_drones = int(line[1])
		except ValueError:
			raise ParsingError("Invalid nb_drones")
		if nb_drones <= 0:
			raise ParsingError("The value should be positive !")
		
	def parse_start_zone(self, line: str) -> None:
		pass
	def parse_end_zone(self, line: str) -> None:
		pass
	def parse_zone(self, line: str) -> None:
		pass
	def parse_connection(self, line: str) -> None:
		pass
