import platform
import psutil
import socket
import time
import uuid

def get_status(model):
    return {
        "timestamp": int(time.time()),
        "hostname": socket.gethostname(),
        "device_id": get_device_id(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "disk_usage": f"{psutil.disk_usage('/').percent}%",
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "model": get_model_metadata(model)
    }

def get_model_metadata(model):
    return {
        "type": str(model.__class__.__name__),
        "framework": "pytorch",  # or detect dynamically later
        "version": getattr(model, '__version__', "1.0.0"),  # customizable
        "hash": "fake_hash_123abc"  # placeholder for checksum or git SHA
    }

def get_device_id():
    # Use persistent unique identifier logic later (e.g., UUID stored on device)
    return str(uuid.getnode())  # MAC address fallback