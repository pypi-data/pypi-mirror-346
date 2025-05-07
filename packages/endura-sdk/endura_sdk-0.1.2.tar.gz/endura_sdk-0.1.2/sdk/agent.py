import psutil

class DeviceAgent:
    def __init__(self, model):
        self.model = model

    def get_status(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        return {
            "status": "Model is not ready and operational",
            "model_type": str(self.model.__class__.__name__),
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%"
        }