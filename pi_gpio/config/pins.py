import yaml
from .gpio import BaseGPIO

PINS_YML = './config/pins.yml'


class PinManager(BaseGPIO):

    def __init__(self):
        super(PinManager, self).__init__()
        self.load_yaml()
        self.initialize_pins()

    def load_yaml(self):
        with open(PINS_YML) as file_data:
            self.__pins = yaml.safe_load(file_data)

    def initialize_pins(self):
        for pin_num, pin_config in self.__pins.items():
            initial = pin_config.get('initial', 'LOW')
            resistor = pin_config.get('resistor', None)
            self.setup_pin(pin_num, pin_config['mode'], initial, resistor)

    def setup_pin(self, num, mode, initial, resistor):
        mode = self.gpio.__getattribute__(mode)
        initial = self.gpio.__getattribute__(initial)
        if resistor:
            resistor = self.gpio.__getattribute__(resistor)
            self.gpio.setup(num, mode, initial=initial, pull_up_down=resistor)
        else:
            self.gpio.setup(num, mode, initial=initial)

    def read_all(self):
        results = []
        for pin_num, pin_config in self.__pins.items():
            pin_read = pin_config.copy()
            pin_read['value'] = self.gpio.input(pin_num)
            results.append(pin_read)
        return results

    def read(self, num):
        pin_num = int(num)
        try:
            pin_read = self.__pins[pin_num].copy()
            pin_read['value'] = self.gpio.input(pin_num)
            return pin_read
        except KeyError:
            return None

    def update(self, num, value):
        pin_num = int(num)
        try:
            self.__pins[pin_num]
            self.gpio.output(pin_num, value)
            return self.read(pin_num)
        except KeyError:
            return None