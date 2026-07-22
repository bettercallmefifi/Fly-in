"""Module to handle the graphical visualization of the drone simulation."""
import math
import pygame
import sys
from typing import Dict, Tuple, Any


class Visualizer:
    """Manages the Pygame window and renders the graph and drones."""

    def __init__(self, width: int = 1900, height: int = 1000) -> None:
        """Initialize Pygame, display settings, and fonts."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Drone Routing Simulation Visualizer")

        self.font = pygame.font.SysFont("Arial", 12, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 22)
        self.drone_font = pygame.font.SysFont("Arial", 10, bold=True)
        self.clock = pygame.time.Clock()

        self.node_radius = 12

    def get_scaled_coords(self, graph: Any) -> Dict[str, Tuple[int, int]]:
        """Calculate dynamic screen coordinates to fit the entire graph."""
        zones = list(graph.zones.values())
        min_x = min(z.x for z in zones)
        max_x = max(z.x for z in zones)
        min_y = min(z.y for z in zones)
        max_y = max(z.y for z in zones)

        range_x = max(max_x - min_x, 1)
        range_y = max(max_y - min_y, 1)

        padding = 120

        scale_x = (self.width - 2 * padding) / range_x
        scale_y = (self.height - 2 * padding) / range_y
        scale = min(scale_x, scale_y)

        offset_x = (self.width - (range_x * scale)) / 2
        offset_y = (self.height - (range_y * scale)) / 2

        scaled = {}
        for z in zones:
            sx = offset_x + (z.x - min_x) * scale
            sy = offset_y + (z.y - min_y) * scale
            scaled[z.name] = (int(sx), int(sy))
        return scaled

    def resolve_color(self, color_name: str) -> Tuple[int, int, int]:
        """Convert a color name or hex string to RGB using Pygame natively."""
        try:
            c = pygame.Color(color_name)
            return (c.r, c.g, c.b)
        except ValueError:
            # if the color name dosen't exist return a default color
            return (200, 200, 200)

    def get_drone_positions(
            self,
            snapshot: Any,
            scaled_coords: Dict[str, Tuple[int, int]]
            ) -> Dict[str, Tuple[int, int]]:
        """Determine the precise pixel location for drones in a given turn."""
        drones_by_zone, drones_on_links, _, _ = snapshot
        positions = {}

        for z_name, d_list in drones_by_zone.items():
            p = scaled_coords[z_name]
            n_drones = len(d_list)
            for i, d_id in enumerate(d_list):
                if n_drones == 1:
                    positions[d_id] = p
                else:
                    angle = i * (2 * math.pi / n_drones)
                    radius = 16 + (n_drones * 1.5)
                    positions[d_id] = (
                        int(p[0] + radius * math.cos(angle)),
                        int(p[1] + radius * math.sin(angle)))

        for (z1, z2), d_list in drones_on_links.items():
            p1 = scaled_coords[z1]
            p2 = scaled_coords[z2]
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            n_drones = len(d_list)
            for i, d_id in enumerate(d_list):
                if n_drones == 1:
                    positions[d_id] = (int(mid_x), int(mid_y))
                else:
                    angle = i * (2 * math.pi / n_drones)
                    radius = 12 + (n_drones * 1.5)
                    positions[d_id] = (
                        int(mid_x + radius * math.cos(angle)),
                        int(mid_y + radius * math.sin(angle)))

        return positions

    def draw_state(
            self,
            sim: Any,
            display_index: int,
            anim_from_index: int,
            t: float
    ) -> None:
        """Render the complete graphical state for
        the current simulation frame."""
        self.screen.fill((30, 30, 40))
        coords = self.get_scaled_coords(sim.graph)

        curr_snapshot = sim.history[display_index]
        prev_snapshot = sim.history[anim_from_index]
        _, _, zone_counts, link_counts = curr_snapshot

        for conn in sim.graph.connections:
            p1 = coords[conn.zone1]
            p2 = coords[conn.zone2]
            current_on_link = link_counts.get((conn.zone1, conn.zone2), 0)

            if current_on_link >= conn.capacity:
                color = (255, 60, 60)
                width = 4
            else:
                color = (80, 120, 160)
                width = 2

            pygame.draw.line(self.screen, color, p1, p2, width)

        for name, zone in sim.graph.zones.items():
            p = coords[name]
            color = self.resolve_color(zone.color)
            current_occupancy = zone_counts.get(name, 0)

            pygame.draw.circle(self.screen, color, p, self.node_radius)
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                p,
                self.node_radius,
                1
            )

            label = f"{name} [{current_occupancy}/{zone.max_drones}]"
            text_surface = self.font.render(label, True, (220, 230, 255))
            rotated_surface = pygame.transform.rotate(text_surface, 45)

            text_rect = rotated_surface.get_rect(
                bottomleft=(p[0] + 5, p[1] - 5)
            )
            self.screen.blit(rotated_surface, text_rect)

        prev_positions = self.get_drone_positions(prev_snapshot, coords)
        curr_positions = self.get_drone_positions(curr_snapshot, coords)

        for d_id, (cx, cy) in curr_positions.items():
            px, py = prev_positions.get(d_id, (cx, cy))

            x = int(px + (cx - px) * t)
            y = int(py + (cy - py) * t)

            drone_color = ((0, 255, 100)
                           if (cx, cy) == coords[sim.graph.end_zone.name]
                           else (255, 165, 0)
                           )
            pygame.draw.circle(self.screen, drone_color, (x, y), 9)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 9, 1)

            d_text = self.drone_font.render(d_id, True, (0, 0, 0))
            d_rect = d_text.get_rect(center=(x, y))
            self.screen.blit(d_text, d_rect)

        info_text = f"Turn: {display_index} | Total Drones: {sim.total_drones}"
        info_surface = self.info_font.render(info_text, True, (255, 200, 0))
        self.screen.blit(info_surface, (20, 20))

        inst_text = "-> /SPACE/ENTER: Next Turn| <-: Previous Turn| ESC: Quit"
        inst_surface = self.info_font.render(inst_text, True, (150, 255, 150))
        self.screen.blit(inst_surface, (self.width - 650, 20))

        pygame.display.flip()

    def run(self, sim: Any) -> None:
        """Start the Pygame main loop and handle user navigation events."""
        display_index = 0
        anim_from_index = 0
        total_steps = len(sim.history)

        TRANSITION_MS = 250.0
        elapsed = TRANSITION_MS

        running = True
        while running:
            dt = self.clock.tick(60)
            elapsed = min(elapsed + dt, TRANSITION_MS)
            t = elapsed / TRANSITION_MS

            self.draw_state(sim, display_index, anim_from_index, t)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (
                        pygame.K_RIGHT, pygame.K_SPACE, pygame.K_RETURN
                    ):
                        if display_index < total_steps - 1:
                            anim_from_index = display_index
                            display_index += 1
                            elapsed = 0
                        else:
                            running = False
                    elif event.key in (pygame.K_LEFT, pygame.K_BACKSPACE):
                        if display_index > 0:
                            anim_from_index = display_index
                            display_index -= 1
                            elapsed = 0

        pygame.quit()
        sys.exit()
