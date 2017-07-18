import importlib.util

class device(object):
    def __init__(self, properties):
       self.properties = properties

    def initialize_driver(self):
        if 'driver' in self.properties:
            print(self.properties['driver'])
            spec = importlib.util.find_spec(self.properties['driver'])
            driver = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(driver)


    def __str__(self):
        if 'name' in self.properties:
            return self.properties['name']
        else:
            return "Device with no name"

if __name__ == "__main__":
    from pharos.model.lib.general_functions import from_yaml_to_devices

    d = from_yaml_to_devices('../../config/devices.yml', name='NI-DAQ')[0]
    d.initialize_driver()
    print(d)