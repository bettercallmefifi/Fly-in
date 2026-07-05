from graph import Graph
from typing import Tuple, Dict


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.zone_names = set()
        self.seen_connections = set()

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
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            lower_line = line.lower()
            if lower_line.startswith("nb_drones:"):
                if nb_drone_exist:
                    raise ParsingError("nb_drones already exist !")
                self.parse_nb_drones(line)
                nb_drone_exist = True

            elif lower_line.startswith("start_hub:"):
                if start_zone_exist:
                    raise ParsingError("start_hub already exist !")
                self.parse_zone(line)
                start_zone_exist = True

            elif lower_line.startswith("end_hub:"):
                if end_zone_exist:
                    raise ParsingError("end_hub already exist !")
                self.parse_zone(line)
                end_zone_exist = True

            elif lower_line.startswith("hub:"):
                self.parse_zone(line)

            elif lower_line.startswith("connection:"):
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
            data = self.valid_metadata_hub(metadata_string)
            print(data)
        else:
            base_data = data_list

        base_elements = base_data.split()
        if len(base_elements) != 3:
            raise ParsingError(
                f"Expected <name> <x> <y>, got: {base_elements}"
                )

        name = base_elements[0]
        t = self.valid_name(name)
        if not t:
            raise ParsingError(f"Dashes are forbidden in zone names: '{name}'")
        X, Y = self.valid_xy(base_elements[1], base_elements[2])

        self.zone_names.add(name)

    def parse_connection(self, line: str) -> None:
        data = 1
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
            data = self.valid_metadata_connection(metadata_string)

        else:
            base_data = data_list
        base_elements = base_data.split("-", 1)

        if len(base_elements) != 2:
            raise ParsingError(
                "Invalid connection format: expected <name1>-<name2>,"
                f" got '{base_elements}'"
                )

        name1 = base_elements[0].strip()
        name2 = base_elements[1].strip()
        zone1 = self.valid_name(name1)
        zone2 = self.valid_name(name2)

        if not zone1 or not zone2:
            raise ParsingError(
                "Dashes are forbidden in zone names !"
                )

        if name1 not in self.zone_names:
            raise ParsingError(
                f"Connection error: Zone '{name1}' does not exist!"
                )
        if name2 not in self.zone_names:
            raise ParsingError(
                f"Connection error: Zone '{name2}' does not exist!"
                )
        if name1 == name2:
            raise ParsingError(
                f"Connection error: Cannot connect zone '{name1}' to itself!"
                )

        connection_pair = frozenset([name1, name2])

        if connection_pair in self.seen_connections:
            raise ParsingError(
                f"Duplicate connection detected between {name1} and {name2}!"
                )

        self.seen_connections.add(connection_pair)

    def valid_name(self, name: str) -> bool:
        if "-" in name:
            return False
        return True

    def valid_xy(self, x: str, y: str) -> Tuple[int, int]:
        try:
            X = int(x)
            Y = int(y)
        except ValueError:
            raise ParsingError("Invalid Coordinates !")
        return X, Y

    def valid_metadata_hub(self, metadata: str) -> Dict[str, str | int]:
        print(metadata)

    def valid_metadata_connection(self, metadata: str) -> int:
        if not metadata:
            raise ParsingError("Metadata is empty !")

        data = metadata.split(" ", 1)
        if len(data) > 1:
            raise ParsingError(
                "Invalid metadata: most be contain just max_link_capacity !"
                )
        value = data[0].split("=", 1)
        if value[0] == "max_link_capacity":
            if len(value) != 2:
                raise ParsingError(
                    f"Invalid metadata format: '{data[0]}' "
                    "is missing an '=' and a value!"
                    )
            try:
                max_capacity = int(value[1])
            except ValueError:
                raise ParsingError(
                    "Invalid metadata: max must be integer !"
                    )
            if max_capacity < 1:
                raise ParsingError(
                    "Invalid metadata: max must be positive !"
                    )
        else:
            raise ParsingError(
                "Invalid metadata: 'max_link_capacity' not exist"
                )

        return max_capacity
