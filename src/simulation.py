from drone import Drone
from graph import Graph
from typing import List, Any, Set


class Simulation:
    def __init__(
            self,
            graph: Graph,
            total_drones: int,
            best_paths: List[List[Any]]
            ) -> None:
        self.graph = graph
        self.total_drones = total_drones
        self.best_paths = best_paths
        self.drones: List[Drone] = []
        self.turns = 0

        self.delayed_drones: Set[str] = set()

        self._initialize_drones()

    def _initialize_drones(self) -> None:
        path_index = 0
        for i in range(1, self.total_drones + 1):
            drone_id = f"D{i}"
            chosen_path = self.best_paths[path_index % len(self.best_paths)]
            new_drone = Drone(drone_id, chosen_path)
            self.drones.append(new_drone)
            path_index += 1

    def run(self, visualizer: Any = None) -> None:
        print("\n================ SIMULATION ==============")
        all_arrived = False

        while not all_arrived:
            if visualizer:
                advance = visualizer.handle_events()
                visualizer.draw_state(self)
                if not advance:
                    continue

            self.turns += 1
            moves_this_turn = []
            all_arrived = True

            for conn in self.graph.connections:
                conn.drones_on_link = 0

            active_drones = [d for d in self.drones if d.status != "arrived"]
            if not active_drones:
                break

            all_arrived = False
            active_drones.sort(key=lambda d: d.current_step, reverse=True)

            for drone in active_drones:
                current_zone = drone.get_current_zone()
                next_zone = drone.get_next_zone()

                if current_zone and next_zone:
                    conn = self.graph.get_connection(
                        current_zone.name, next_zone.name
                        )
                    is_end_zone = (next_zone.name == self.graph.end_zone.name)

                    zone_has_space = is_end_zone or (
                        next_zone.current_drones_inside < next_zone.max_drones
                        )
                    conn_has_space = (conn is not None) and (
                        conn.drones_on_link < conn.capacity
                        )
                    if drone.id in self.delayed_drones:
                        if conn_has_space:
                            drone.move()
                            self.delayed_drones.remove(drone.id)
                            conn.drones_on_link += 1

                    else:
                        if zone_has_space and conn_has_space:

                            if next_zone.zone_type == "restricted":
                                self.delayed_drones.add(drone.id)

                                if current_zone.name != (
                                    self.graph.start_zone.name
                                ):
                                    current_zone.current_drones_inside -= 1

                                if not is_end_zone:
                                    next_zone.current_drones_inside += 1

                                conn.drones_on_link += 1
                                moves_this_turn.append(
                                    f"{drone.id}-{next_zone.name}"
                                    )

                            else:
                                drone.move()

                                if not is_end_zone:
                                    next_zone.current_drones_inside += 1

                                if current_zone.name != (
                                    self.graph.start_zone.name
                                ):
                                    current_zone.current_drones_inside -= 1

                                conn.drones_on_link += 1
                                moves_this_turn.append(
                                    f"{drone.id}-{next_zone.name}"
                                    )

            if moves_this_turn:
                print(" ".join(moves_this_turn))

        if visualizer:
            visualizer.draw_state(self)

        print(f"\nSimulation finished in {self.turns} turns!")
        print("=======================================================")
