"""Simulation module to handle turn-based drone movements."""
from drone import Drone, initialize_drones
from graph import Graph
from typing import List, Any, Set, Dict, Tuple


class Simulation:
    """Manages the execution of the drone routing simulation."""

    def __init__(
            self,
            graph: Graph,
            total_drones: int,
            best_paths: List[List[Any]]
            ) -> None:
        """Initialize the simulation with graph,
        total drones, and best paths."""
        self.graph = graph
        self.total_drones = total_drones
        self.best_paths = best_paths
        self.turns = 0

        self.delayed_drones: Set[str] = set()
        self.history: List[Any] = []

        self.drones: List[Drone] = initialize_drones(
            self.total_drones, self.best_paths
            )

    def capture_snapshot(self) -> Tuple[
            Dict[str, List[str]],
            Dict[Tuple[str, str], List[str]],
            Dict[str, int],
            Dict[Tuple[str, str], int]]:
        """Capture the current state of the graph
        and drones for visualization."""
        assert self.graph.start_zone is not None
        assert self.graph.end_zone is not None

        drones_by_zone: Dict[str, List[str]] = {}
        drones_on_links: Dict[Tuple[str, str], List[str]] = {}

        for drone in self.drones:
            if drone.status == "arrived":
                z_name = self.graph.end_zone.name
                if z_name not in drones_by_zone:
                    drones_by_zone[z_name] = []
                drones_by_zone[z_name].append(drone.id)
            else:
                curr_z = drone.get_current_zone()
                if drone.id in self.delayed_drones:
                    next_z = drone.get_next_zone()
                    if curr_z and next_z:
                        link = (curr_z.name, next_z.name)
                        if link not in drones_on_links:
                            drones_on_links[link] = []
                        drones_on_links[link].append(drone.id)
                else:
                    if curr_z:
                        z_name = curr_z.name
                    else:
                        z_name = self.graph.start_zone.name

                    if z_name not in drones_by_zone:
                        drones_by_zone[z_name] = []
                    drones_by_zone[z_name].append(drone.id)

        zone_counts = {
            name: z.current_drones_inside for
            name, z in self.graph.zones.items()}
        link_counts = {(c.zone1, c.zone2): c.drones_on_link for
                       c in self.graph.connections}

        return (drones_by_zone, drones_on_links, zone_counts, link_counts)

    def run(self) -> None:
        """Execute the turn-by-turn simulation loop."""
        assert self.graph.start_zone is not None
        assert self.graph.end_zone is not None

        print("\n================ SIMULATION ==============")
        self.history.append(self.capture_snapshot())

        while True:
            active_drones = [d for d in self.drones if d.status != "arrived"]
            if not active_drones:
                break

            self.turns += 1
            moves_this_turn = []

            for conn in self.graph.connections:
                conn.drones_on_link = 0

            active_drones.sort(key=lambda d: d.current_step, reverse=True)

            for drone in active_drones:
                current_zone = drone.get_current_zone()
                next_zone = drone.get_next_zone()

                if current_zone and next_zone:
                    conn = self.graph.get_connection(
                        current_zone.name, next_zone.name
                    )
                    is_end_zone = (next_zone.name == self.graph.end_zone.name)

                    # 1. Drone is already in-flight to a restricted zone
                    if drone.id in self.delayed_drones:
                        drone.move()
                        self.delayed_drones.remove(drone.id)

                        # NOTE: We do not increment next_zone occupancy here
                        # because it was already reserved in the previous turn.
                        raw_move = f"{drone.id}-{next_zone.name}"
                        moves_this_turn.append(raw_move)

                    # 2. Drone is looking to move
                    else:
                        zone_has_space = is_end_zone or (
                            next_zone.current_drones_inside <
                            next_zone.max_drones
                        )
                        conn_has_space = (conn is not None) and (
                            conn.drones_on_link < conn.capacity
                        )

                        if conn_has_space and zone_has_space:
                            if next_zone.zone_type == "restricted":
                                self.delayed_drones.add(drone.id)
                                if current_zone.name != (
                                    self.graph.start_zone.name
                                ):
                                    current_zone.current_drones_inside -= 1

                                # Reserve the space in the destination
                                # zone IMMEDIATELY
                                if not is_end_zone:
                                    next_zone.current_drones_inside += 1

                                conn.drones_on_link += 1

                                raw_move = f"{
                                    drone.id
                                    }-{
                                        current_zone.name
                                        }-{
                                            next_zone.name
                                            }"
                                moves_this_turn.append(raw_move)

                            else:
                                drone.move()
                                if not is_end_zone:
                                    next_zone.current_drones_inside += 1
                                if current_zone.name != (
                                    self.graph.start_zone.name
                                ):
                                    current_zone.current_drones_inside -= 1

                                conn.drones_on_link += 1

                                raw_move = f"{drone.id}-{next_zone.name}"
                                moves_this_turn.append(raw_move)

            if moves_this_turn:
                print(" ".join(moves_this_turn))

            self.history.append(self.capture_snapshot())

        print(f"\nSimulation finished in {self.turns} turns!")
        print("=======================================================")
