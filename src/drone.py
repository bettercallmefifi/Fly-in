class Drone:
    def __init__(self, drone_id: str, path: list):
        self.id = drone_id
        self.path = path
        self.current_step = 0
        self.status = "waiting"

    def get_current_zone(self):
        if self.current_step < len(self.path):
            return self.path[self.current_step]
        return None

    def get_next_zone(self):
        if self.current_step + 1 < len(self.path):
            return self.path[self.current_step + 1]
        return None

    def move(self):
        if self.status != "arrived" and self.get_next_zone() is not None:
            self.current_step += 1
            self.status = "moving"

            if self.current_step == len(self.path) - 1:
                self.status = "arrived"
