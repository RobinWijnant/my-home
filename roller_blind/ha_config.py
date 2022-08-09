def get_blind_config(topic):
    return {
        "name": "Window cover",
        "device_class": "blind",
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


def get_calibration_open_button_config(topic):
    return {
        "unique_id": "rpi4-window-roller-blind-calibration-open",
        "name": "Roller blind calibrate open",
        "command_topic": f"{topic}/set",
        "payload_press": "OPEN",
        "availability": {
            "topic": f"{topic}/availability",
            "payload_available": "online",
            "payload_not_available": "offline",
        },
        "entity_category": "config",
        "device_class": "restart",
    }


def get_calibration_closed_button_config(topic):
    return {
        "unique_id": "rpi4-window-roller-blind-calibration-closed",
        "name": "Roller blind calibrate closed",
        "command_topic": f"{topic}/set",
        "payload_press": "CLOSE",
        "availability": {
            "topic": f"{topic}/availability",
            "payload_available": "online",
            "payload_not_available": "offline",
        },
        "entity_category": "config",
        "device_class": "restart",
    }
