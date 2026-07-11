class Drone:
    def __init__(self, drone_id: str, path: list):
        self.id = drone_id
        self.path = path
        self.current_step = 0
        self.status = "waiting"

