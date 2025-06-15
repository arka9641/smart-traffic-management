import random
import time
import requests

while True:
    data = {
        "sensor_id": "sensor_" + str(random.randint(1, 10)),
        "vehicle_count": random.randint(0, 100),
        "avg_speed": random.randint(5, 60)
    }
    requests.post("http://localhost:5000/api/sensor-data", json=data)
    time.sleep(5)