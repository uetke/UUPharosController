"""
This class is created from scratch using the tested measurement.py class on 26/7/17
The goal is to prepare a sandbox experiment on this platform
Section authors: Sanli Faez, Aquiles Carattino
"""

import numpy as np
from time import sleep
#from lantz import Q_
from pharos.model.lib.general_functions import from_yaml_to_devices, from_yaml_to_dict


class measurement(object):
    def __init__(self, measure):
        """Measurement class that will hold all the information regarding the experiment being performed.
        :param measure: a dictionary (as in the python type "dictionary") with the necessary steps
        """
        self.measure = measure  # Dictionary of the measurement steps
        self.devices = {}  # Dictionary holding all the devices
        self.daqs = {}  # Dictionary that holds for each daq the inputs and outputs.

        # This short block is going to become useful in the future, when interfacing with a GUI
        for d in self.measure:
            setattr(self, d, self.measure[d])

    def load_devices(self, source=None):
        """ Loads the devices from the files defined in the INIT part of the yml.
        :param source: Not implemented yet.
        :return:
        """
        if source is not None:
            return
        init = self.measure['init']
        devices_file = init['devices']
        devices_list = from_yaml_to_devices(devices_file)
        for dev in devices_list:
            self.devices[dev.properties['name']] = dev
            print('Added %s to the experiment' % dev)

    def initialize_devices(self):
        """ Initializes the devices first by loading the driver,
        then by applying the default values if they are present.
        :return:
        """
        for k in self.devices:
            dev = self.devices[k]
            print('Starting %s' % dev.properties['name'])
            try:
                dev.initialize_driver()
            except:
                print('Error initializing %s' % dev.properties['name'])
            # if 'defaults' in dev.properties:
            #     defaults_file = dev.properties['defaults']
            #     defaults = from_yaml_to_dict(defaults_file)[dev.properties['name']]
            #     dev.apply_values(defaults)
            if dev.properties['type'] == 'daq':
                self.daqs[dev.properties['name']] = {'input': [],
                                                     'output': [],
                                                     'monitor': [], }  # Creates an entry for every different DAQ.

    def connect_all_devices_to_daq(self):
        """ Iterates through the devices and appends the outputs and inputs to each daq.
        :return: None
        """
        for d in self.devices:
            dev = self.devices[d]  # Get the device from the devices list
            if 'device' in dev.properties['connection']: #checks if a device is connected via another DAQ card, this is notified by defining a "nested device" in the connection property of the "sensory device"
                connected_to = dev.properties['connection']['device']
                mode = dev.properties['mode'] #can be input or output, will later be useful to create a categorial list
                self.daqs[connected_to][mode].append(dev)
                print('Appended %s to %s' % (dev, connected_to))

    def gen_wave(self):
        """Created by Sanli on 26/7/17 to practice"""
        genwave = self.measure['GenWaveDetect']