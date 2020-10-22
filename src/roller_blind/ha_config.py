def getConfig(topic):
    return {
        "name": "Window cover",
        "unique_id": "window_cover",
        "device_class": "blind",
        "device": {
            "name": "Docker image",
            "model": "Python 3",
            "manufacturer": "Robin Wijnant",
            "identifiers": ("window_cover"),
        },
        "command_topic": f"{topic}/set",
        "position_topic": f"{topic}/position",
        "availability": {
            "topic": f"{topic}/availability",
            "payload_available": "online",
            "payload_not_available": "offline",
        },
        "set_position_topic": f"{topic}/set_position",
        "payload_open": "OPEN",
        "payload_close": "CLOSE",
        "payload_stop": "STOP",
        "position_open": 0,
        "position_closed": 1000,
    }
