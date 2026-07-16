from graph import Graph
from connection import Connection
from zone import Zone
from typing import Tuple, Dict
import random


class ParsingError(Exception):
    pass


class Parser:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.zone_names = set()
        self.seen_connections = set()
        self.positions = set()
        self.total_drones = 0
        self.graph = Graph()

    def parsing(self):
        try:
            with open(self.file_name, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise ParsingError("Choose an existing file !")
        except PermissionError:
            raise ParsingError(
                "Permission denied: Cannot read the file !"
                )
        except IsADirectoryError:
            raise ParsingError(
                "The provided path is a directory, not a file !"
                )

        nb_drone_exist = False
        end_zone_exist = False
        start_zone_exist = False
        is_first_data_line = True
        connections_to_parse = []

        if not lines:
            raise ParsingError("The file is empty !")

        for line_num, original_line in enumerate(lines, start=1):
            try:
                line = original_line.split("#", 1)[0].strip()

                if not line or line.startswith("#"):
                    continue

                lower_line = line.lower()

                if is_first_data_line:
                    if not lower_line.startswith("nb_drones:"):
                        raise ParsingError(
                            "The first valid line in "
                            "the map must be 'nb_drones:' !"
                            )
                    is_first_data_line = False

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
                    if not start_zone_exist:
                        raise ParsingError(
                            "A 'start_hub' must be defined "
                            "before regular hubs !"
                            )
                    if end_zone_exist:
                        raise ParsingError(
                            "An 'end_hub' must be defined after regular hubs !"
                            )
                    self.parse_zone(line)

                elif lower_line.startswith("connection:"):
                    connections_to_parse.append((line_num, line))
                else:
                    raise ParsingError("invalid data !")

            except ParsingError as e:
                raise ParsingError(f"Error on line {line_num}: {e}")

        if not nb_drone_exist:
            raise ParsingError("The map is missing 'nb_drones' !")
        if not end_zone_exist:
            raise ParsingError("The map is missing an 'end_hub' !")

        for line_num, conn_line in connections_to_parse:
            try:
                self.parse_connection(conn_line)
            except ParsingError as e:
                raise ParsingError(f"Error on line {line_num}: {e}")

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

        self.total_drones = nb_drones

    def parse_zone(self, line: str) -> None:
        is_unlimited = (line.lower().startswith("start_hub")
                        or line.lower().startswith("end_hub"))
        is_start = line.lower().startswith("start_hub")
        is_end = line.lower().startswith("end_hub")

        line = line.split(":", 1)

        if len(line) != 2:
            raise ParsingError("Invalid data !")

        data_list = line[1].strip()
        metadata_string = ""
        data = {}

        if data_list.endswith("]"):

            last_bracket_idx = data_list.rfind("[")

            if last_bracket_idx == -1:
                raise ParsingError("Metadata most be start with '['!")

            raw_metadata = data_list[last_bracket_idx + 1:-1]
            if raw_metadata.startswith(" ") or raw_metadata.endswith(" "):
                raise ParsingError(
                    "Invalid metadata:"
                    " spaces just inside the brackets are strictly forbidden !"
                    )

            base_data = data_list[:last_bracket_idx].strip()
            metadata_string = data_list[last_bracket_idx + 1:-1].strip()
            data = self.valid_metadata_hub(metadata_string)
        else:
            base_data = data_list

        base_elements = base_data.split()

        if len(base_elements) != 3:
            raise ParsingError(
                f"Expected <name> <x> <y>, got: {base_elements}"
                )

        name = base_elements[0]
        t = self.valid_name(name)

        if name in self.zone_names:
            raise ParsingError(
                f"Duplicate zone error: The name '{name}' is already used !"
                )

        if not t:
            raise ParsingError(
                f"Dashes are forbidden in zone names: '{name}'"
                )

        self.zone_names.add(name)

        X, Y = self.valid_xy(base_elements[1], base_elements[2])

        if (X, Y) in self.positions:
            raise ParsingError(
                f"Duplicate position error: Coordinates ({X}, {Y})"
                " are already used by another zone !"
            )
        self.positions.add((X, Y))

        if is_unlimited:
            final_max_drones = self.total_drones
        else:
            final_max_drones = data.get("max_drones", 1)

        color = data.get("color", "#FFFFFF")
        zone_type = data.get("zone", "normal")

        new_zone = Zone(name, X, Y, final_max_drones, color, zone_type)
        self.graph.add_zone(new_zone)

        if is_unlimited:
            if is_start:
                self.graph.start_zone = new_zone
            elif is_end:
                self.graph.end_zone = new_zone

    def parse_connection(self, line: str) -> None:
        data = 1
        line = line.split(":", 1)

        if len(line) != 2:
            raise ParsingError("Invalid data !")

        data_list = line[1].strip()
        metadata_string = ""

        if data_list.endswith("]"):
            last_bracket_idx = data_list.rfind("[")

            if last_bracket_idx == -1:
                raise ParsingError("Metadata most start with '['!")

            raw_metadata = data_list[last_bracket_idx + 1:-1]
            if raw_metadata.startswith(" ") or raw_metadata.endswith(" "):
                raise ParsingError(
                    "Invalid metadata:"
                    " spaces just inside the brackets are strictly forbidden !"
                    )

            base_data = data_list[:last_bracket_idx].strip()
            metadata_string = data_list[last_bracket_idx + 1:-1].strip()
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
        new_conn = Connection(name1, name2, data)
        self.graph.add_connection(new_conn)

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
        metadata_allowed = ["zone", "color", "max_drones"]
        types_allowed = ["normal", "blocked", "restricted", "priority"]
        parsed_data: Dict[str, str | int] = {}
        color_code = {
                "green": "#008000", "red": "#FF0000",
                "purple": "#800080",
                "black": "#000000", "brown": "#A52A2A",
                "orange": "#FFA500",
                "maroon": "#800000", "gold": "#FFD700",
                "darkred": "#8B0000",
                "violet": "#EE82EE", "crimson": "#DC143C",
                "rainbow": "#FF00FF",
                "blue": "#0000FF", "yellow": "#FFFF00",
                "cyan": "#00FFFF",
                "lime": "#00FF00", "magenta": "#FF00FF",
                "white": "#FFFFFF",
                "gray": "#808080", "silver": "#C0C0C0",
                "pink": "#FFC0CB",
                "teal": "#008080", "navy": "#000080",
                "olive": "#808000",
                "coral": "#FF7F50", "salmon": "#FA8072",
                "khaki": "#F0E68C",
                "plum": "#DDA0DD", "indigo": "#4B0082",
                "turquoise": "#40E0D0",
                "azure": "#F0FFFF", "chocolate": "#D2691E",
                "tomato": "#FF6347",
                "orchid": "#DA70D6", "slate": "#708090",
                "beige": "#F5F5DC",
                "mint": "#98FF98", "lavender": "#E6E6FA",
                "peach": "#FFDAB9"
            }

        if not metadata:
            raise ParsingError("Metadata is empty !")

        if " =" in metadata or "= " in metadata:
            raise ParsingError(
                "Invalid metadata: spaces around '=' are strictly forbidden !"
                )

        items = metadata.split()
        for item in items:
            if "=" not in item:
                raise ParsingError(f"Invalid data: missing = in {item}")

            detail, value = item.split("=", 1)

            if detail in parsed_data:
                raise ParsingError(
                    f"Duplicate metadata error: '{detail}' is "
                    "defined more than once !"
                    )

            if detail not in metadata_allowed:
                raise ParsingError("There is no metadata allowed !")

            if detail == "zone":
                if value not in types_allowed:
                    raise ParsingError(
                        "Invalid metadata: the type not allowed !"
                        )
                parsed_data[detail] = value

            elif detail == "color":
                if not value:
                    raise ParsingError(
                        "Invalid metadata: color value cannot be empty!"
                        )
                safe_color_name = value.lower()

                if safe_color_name in color_code:
                    hex_value = color_code[safe_color_name]
                else:
                    all_hex_colors = list(color_code.values())
                    hex_value = random.choice(all_hex_colors)
                parsed_data[detail] = hex_value

            elif detail == "max_drones":
                try:
                    max_drones = int(value)
                except ValueError:
                    raise ParsingError(
                        "invalid metadata: max_drone most be an integer !"
                        )
                if max_drones <= 0:
                    raise ParsingError(
                        "Invalid metadata: max_drone most be positive !"
                        )
                parsed_data[detail] = max_drones

        return parsed_data

    def valid_metadata_connection(self, metadata: str) -> int:
        if not metadata:
            raise ParsingError("Metadata is empty !")

        if " =" in metadata or "= " in metadata:
            raise ParsingError(
                "Invalid metadata: spaces around '=' are strictly forbidden !"
                )

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
