class Drone:
    def __init__(self, drone_id: int, start_zone: str):
        self.id = drone_id
        self.current_zone = start_zone
        self.path = []
        self.is_done = False
