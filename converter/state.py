from .config import Config


class State:
    def __init__(self, config: Config):
        self.config = config
        self.max_height = 0.0
        self.next_id = 0
        self.is_directed = False
