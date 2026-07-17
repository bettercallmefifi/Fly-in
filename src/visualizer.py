import math
import pygame
import sys
from typing import Dict, Tuple, Any, List


class Visualizer:
    def __init__(self, width: int = 1400, height: int = 900) -> None:
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

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        try:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b)
        except ValueError:
            return (200, 200, 200)

    def draw_state(self, sim: Any) -> None:
        self.screen.fill((30, 30, 40))
        coords = self.get_scaled_coords(sim.graph)

        for conn in sim.graph.connections:
            p1 = coords[conn.zone1]
            p2 = coords[conn.zone2]

            if conn.drones_on_link >= conn.capacity:
                color = (255, 60, 60)
                width = 4
            else:
                color = (80, 120, 160)
                width = 2

            pygame.draw.line(self.screen, color, p1, p2, width)

        for name, zone in sim.graph.zones.items():
            p = coords[name]
            color = self.hex_to_rgb(zone.color)

            pygame.draw.circle(self.screen, color, p, self.node_radius)
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                p,
                self.node_radius,
                1
            )

            label = f"{name} [{zone.current_drones_inside}/{zone.max_drones}]"
            text_surface = self.font.render(label, True, (220, 230, 255))
            rotated_surface = pygame.transform.rotate(text_surface, 45)

            text_rect = rotated_surface.get_rect(
                bottomleft=(p[0] + 5, p[1] - 5)
            )
            self.screen.blit(rotated_surface, text_rect)

        drones_by_zone: Dict[str, List[str]] = {}
        drones_on_links: Dict[Tuple[str, str], List[str]] = {}

        for drone in sim.drones:
            if drone.status == "arrived":
                z_name = sim.graph.end_zone.name
                if z_name not in drones_by_zone:
                    drones_by_zone[z_name] = []
                drones_by_zone[z_name].append(drone.id)
            else:
                curr_z = drone.get_current_zone()

                if (
                    hasattr(sim, 'delayed_drones')
                    and drone.id in sim.delayed_drones
                ):
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
                        z_name = sim.graph.start_zone.name

                    if z_name not in drones_by_zone:
                        drones_by_zone[z_name] = []
                    drones_by_zone[z_name].append(drone.id)

        for z_name, d_list in drones_by_zone.items():
            if not d_list:
                continue

            p = coords[z_name]
            n_drones = len(d_list)

            for i, d_id in enumerate(d_list):
                if n_drones == 1:
                    dx, dy = p[0], p[1]
                else:
                    angle = i * (2 * math.pi / n_drones)
                    radius = 16 + (n_drones * 1.5)
                    dx = int(p[0] + radius * math.cos(angle))
                    dy = int(p[1] + radius * math.sin(angle))

                drone_color = (0, 255, 100)
                pygame.draw.circle(
                    self.screen, drone_color, (int(dx), int(dy)), 9
                )
                pygame.draw.circle(
                    self.screen, (0, 0, 0), (int(dx), int(dy)), 9, 1
                )

                d_text = self.drone_font.render(d_id, True, (0, 0, 0))
                d_rect = d_text.get_rect(center=(int(dx), int(dy)))
                self.screen.blit(d_text, d_rect)

        for (z1, z2), d_list_links in drones_on_links.items():
            if not d_list_links:
                continue

            p1 = coords[z1]
            p2 = coords[z2]

            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2

            n_drones = len(d_list_links)
            for i, d_id in enumerate(d_list_links):
                if n_drones == 1:
                    dx, dy = mid_x, mid_y
                else:
                    angle = i * (2 * math.pi / n_drones)
                    radius = 12 + (n_drones * 1.5)
                    dx = int(mid_x + radius * math.cos(angle))
                    dy = int(mid_y + radius * math.sin(angle))

                drone_color = (255, 165, 0)
                pygame.draw.circle(
                    self.screen, drone_color, (int(dx), int(dy)), 9
                )
                pygame.draw.circle(
                    self.screen, (0, 0, 0), (int(dx), int(dy)), 9, 1
                )

                d_text = self.drone_font.render(d_id, True, (0, 0, 0))
                d_rect = d_text.get_rect(center=(int(dx), int(dy)))
                self.screen.blit(d_text, d_rect)

        info_text = f"Turn: {sim.turns} | Total Drones: {sim.total_drones}"
        info_surface = self.info_font.render(info_text, True, (255, 200, 0))
        self.screen.blit(info_surface, (20, 20))

        inst_text = "[SPACE] button make the dorne move"
        inst_surface = self.info_font.render(inst_text, True, (150, 255, 150))
        self.screen.blit(inst_surface, (self.width - 400, 20))

        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self) -> bool:
        advance_turn = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    advance_turn = True
        return advance_turn
