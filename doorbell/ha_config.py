import os


def get_button_config(topic):
    return {
        "automation_type": "trigger",
        "topic": f"{topic}/press",
        "type": "button_short_press",
        "device": {
            "identifiers": os.getenv("DEVICE_ID"),
            "manufacturer": "Portainer",
            "model": "Python 3.8",
            "name": "Doorbell container",
        },
    }


def get_main_button_config(topic):
    button_config = get_button_config(topic)
    button_config.update(
        {"subtype": "button_1",}
    )
    return button_config


def get_guest_button_config(topic):
    button_config = get_button_config(topic)
    button_config.update(
        {"subtype": "button_2",}
    )
    return button_config
