"""
    Place to store general functions that may be used throwout the program.
"""
import yaml
from pharos.model.lib.device import device

def from_yaml_to_devices(filename = "config/devices.yml", mod=None):
    """ Reads a YAML file and returns a list of devices.
    :param filename: File where the data is stored
    :param mod: The type of device to look for
    :return: list of :class: device
    """

    stream = open(filename, 'r')
    devices = yaml.load(stream)['devices']
    print(devices)
    stream.close()
    devs = []
    for d in devices:
        if mod != None:
            if devices[d]['type'] == mod:
                for dev in devices[d]['devices']:
                    dd = device(devices[d]['devices'][dev])
                    devs.append(dd)
                    print(dd)
        else:
            for dev in devices[d]['devices']:
                dd = device(devices[d]['devices'][dev])
                devs.append(dd)
                print(dd)
    return devs

if __name__ == "__main__":
    d = from_yaml_to_devices('../../config/devices.yml', mod='NI-DAQ')
    print(d)