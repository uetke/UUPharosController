"""
    Place to store general functions that may be used throwout the program.
"""
import yaml
from pharos.model.lib.device import device

def from_yaml_to_devices(filename = "config/devices.yml", mod=None):
    """ Reads a YAML file and returns a list of devices.
    :param filename: File where the data is stored
    :param mod: The type of device to look for, for example: {'connection': {'device': 'NI-DAQ'}}
    :return: list of :class: device
    """

    stream = open(filename, 'r')
    devices = yaml.load(stream)

    stream.close()
    devs = []
    for d in devices:
        dev = devices[d]
        if mod is not None:
            k = list(mod.keys())[0] # Extract the key from the condition
            print(k)
            v = mod[k]
            print(v)
            try:
                if dev[k] == v:
                    dd = device(dev)
                    devs.append(dd)
                    print(dd)
            except:
                print('except')
                pass
        else:
            dd = device(dev)
            devs.append(dd)
            print(dd)
    return devs

if __name__ == "__main__":
    d = from_yaml_to_devices('../../config/devices.yml',mod={'connection': {'type': 'daq'}})
   # print(d)