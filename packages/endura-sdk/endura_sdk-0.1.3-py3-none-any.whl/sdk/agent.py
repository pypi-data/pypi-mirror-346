from .core import get_status

class DeviceAgent:
    def __init__(self, model):
        self.model = model

    def get_status(self):
        return get_status(self.model)