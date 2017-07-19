from pharos.model.lib.general_functions import from_yaml_to_devices, from_yaml_to_dict

class measurement(object):
    def __init__(self, measure):
        """Measurement class that will hold all the information regardin the experiment being performed.
        :param measure: a dictionary with the necessary steps
        """
        self.measure = measure
        self.devices = []

    def initialize_devices(self):
        init_steps = self.measure['init']
        devices_file = init_steps['devices']
        self.devices = from_yaml_to_devices(devices_file)
        for dev in self.devices:
            if 'defaults' in dev:
                defaults_file = dev['defaults']
                defaults = from_yaml_to_dict(defaults_file)
