from rpi_rf import RFDevice


class RadioSwitch:
    DATA_PIN = 27

    def __init__(self):
        self.rf_device = RFDevice(RadioSwitch.DATA_PIN)
        self.rf_device.enable_rx()
        self.last_read_timestamp = None

    def __del__(self):
        self.rf_device.cleanup()

    def is_available(self):
        if self.rf_device.rx_code_timestamp != self.last_read_timestamp:
            self.last_read_timestamp = self.rf_device.rx_code_timestamp
            return True
        return False

    def read(self):
        return {
            "code": self.rf_device.rx_code,
            "pulse_length": self.rf_device.rx_pulselength,
            "protocol": self.rf_device.rx_proto,
        }

