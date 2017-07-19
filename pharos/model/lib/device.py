class device(object):
    def __init__(self, properties):
        self.properties = properties
        self.driver = None
        self.params = {}

    def add_driver(self, driver):
        """ Adds the driver of the device. It has to be initialized()
        :param driver: driver of any class.
        :return: Null
        """
        self.driver = driver

    def apply_values(self, values):
        """ Iterates over all values of a dictionary and sets the values of the driver to it.
        :param values: a dictionary
        :return:
        """
        if isinstance(values, dict):
            for k in values:
                print('Setting %s to %s'%(k, values[k]))
                setattr(self.driver, k, values[k])
            self.params[k] = values[k]
        else:
            raise Exception('Drivers can only update dictionaries')

    def get_params(self):
        return self.params

    def __str__(self):
        if 'name' in self.properties:
            return self.properties['name']
        else:
            return "Device with no name"

if __name__ == "__main__":
    from pharos.model.lib.general_functions import from_yaml_to_devices

    d = from_yaml_to_devices('../../config/devices.yml', name='NI-DAQ')[0]
    print(d)