from graph import Graph
from typing import Tuple, Dict

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
                self.parse_zone(line)
                start_zone_exist = True

            elif line.startswith("end_hub:"):
                if end_zone_exist:
                    raise ParsingError("end_hub already exist !")
                self.parse_zone(line)
                end_zone_exist = True

            elif line.startswith("hub:"):
                self.parse_zone(line)

            elif line.startswith("connection:"):
                self.parse_connection(line)
            else:
                raise ParsingError("There is no data !")

    def parse_nb_drones(self, line: str) -> None:
        line = line.split(":")
        if len(line) != 2:
            raise ParsingError("Invalid data !")
        try:
            nb_drones = int(line[1].strip())
        except ValueError:
            raise ParsingError("Invalid nb_drones")
        if nb_drones <= 0:
            raise ParsingError("The value should be positive !")
        # self.graph.nb_drones = nb_drones		

    def parse_zone(self, line: str) -> None:
        line = line.split(":", 1)
        if len(line) != 2:
            raise ParsingError("Invalid data !")
        data_list = line[1].strip()
        metadata_string = ""
        if "[" in data_list:
            if not data_list.endswith("]"):
                raise ParsingError("Metadata most be closed with ']'!")

            base_data, meta_part = data_list.split("[", 1)
            metadata_string = meta_part.replace("]", "").strip()
        else:
            base_data = data_list

        base_elements = base_data.split()
        if len(base_elements) != 3:
            raise ParsingError(f"Expected <name> <x> <y>, got: {base_elements}")

        name = base_elements[0]
        if "-" in name:
            raise ParsingError(f"Dashes are forbidden in zone names: '{name}'")
        X, Y = self.valid_xy(base_elements[1], base_elements[2])
        print(X, Y)


    def parse_connection(self, line: str) -> None:
        pass

    def valid_xy(self, x: str, y: str) -> Tuple[int, int]:
        try:
            X = int(x)
            Y = int(y)
        except ValueError:
            raise ParsingError("Invalid Coordinates !")
        return X, Y
	
    def valid_metadata(self, metadata: str) -> Dict[str, str | int]:
        pass
