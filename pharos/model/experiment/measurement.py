import sys
import numpy as np
from time import sleep
from lantz import Q_
from pharos.model.lib.general_functions import from_yaml_to_devices, from_yaml_to_dict

class measurement(object):
    def __init__(self, measure):
        """Measurement class that will hold all the information regardin the experiment being performed.
        :param measure: a dictionary with the necessary steps
        """
        self.measure = measure
        self.devices = {}

    def load_devices(self, source=None):
        if source is not None:
            return
        init = self.measure['init']
        devices_file = init['devices']
        devices_list = from_yaml_to_devices(devices_file)
        for dev in devices_list:
            self.devices[dev.properties['name']] = dev
            print('Added %s to the experiment' % dev)

    def initialize_devices(self):
        for k in self.devices:
            dev = self.devices[k]
            print('Starting %s' % dev.properties['name'])
            try:
                dev.initialize_driver()
            except:
                print('Error initializing %s' % dev.properties['name'])
                #pass
            if 'defaults' in dev.properties:
                defaults_file = dev.properties['defaults']
                defaults = from_yaml_to_dict(defaults_file)[dev.properties['name']]
                dev.apply_values(defaults)

    def do_scan(self):
        daqs = {}
        scan = self.measure['scan']
        devices_to_monitor = scan['detectors']
        # Check the devices
        print('Going to monitor:')
        for dev in devices_to_monitor:
            dev = self.devices[dev]  # Get the input device from the devices list
            print('\t- %s' % dev)
            connection = dev.properties['connection']
            if connection['type'] == 'daq':
                if not connection['device'] in daqs:
                    daqs[connection['device']] = [dev]
                else:
                    daqs[connection['device']].append(dev)

        # Sets up the laser
        laser_params = scan['laser']
        laser = self.devices[laser_params['name']]
        try:
            laser.apply_values(laser_params)
        except:
            print('Problem changing values of the laser')

        num_points = int((laser.params['stop_wavelength']-laser.params['start_wavelength'])/laser.params['trigger_step'] )
        accuracy = laser.params['trigger_step']/laser.params['speed']
        conditions = {
            'accuracy': accuracy,
            'points': -1
        }

        for d in daqs:
            daq = self.devices[d]  # Get the DAQ from the devices list
            devs = daqs[d]  # daqs dictionary groups the channels by daq to which they are plugged
            conditions['devices'] = devs
            conditions['trigger'] = daq.properties['trigger']
            conditions['trigger_source'] = daq.properties['trigger_source']
            daq.driver.analog_input_setup(conditions)
            self.devices[d].driver.trigger_analog()

        axis = scan['axis']
        approx_time_to_scan = (laser.params['stop_wavelength']-laser.params['start_wavelength'])/laser.params['speed']
        print('Total number of devices to scan: %s' % len(axis))
        data_scan = {}
        for dev_to_scan in axis:
            # Set all the devices to their default value
            for dev_name in axis:
                if dev_name != 'time':
                    value = Q_(axis[dev_name]['default'])
                    self.set_value_to_device(dev_name, value)

            # Scan the laser and the values of the given device
            if dev_to_scan != 'time':
                dev_range = axis[dev_to_scan]['range']
                start = Q_(dev_range[0])
                stop = Q_(dev_range[1])
                step = Q_(dev_range[2])
                num_points_dev = ((stop-start)/step).to('')
            else:
                start = 1
                stop = axis['time']['repetitions']
                num_points_dev = stop
            data_scan[dev_to_scan] = {}
            for value in np.linspace(start, stop, num_points_dev):
                self.set_value_to_device(dev_to_scan, value*Q_('um')) ### ATTENTION HERE!!!!
                for d in daqs:
                    
                    pass
                laser.driver.execute_sweep()
                sleep(10)
                while laser.driver.sweep_condition != 'Stop':
                    sleep(approx_time_to_scan/10)
                conditions = {
                    'points': 0,
                }
                for d in daqs:
                    v, dd = self.devices[d].driver.read_analog(None, conditions)
                    data_scan[dev_to_scan][d] = dd
                    print('Acquired data!')
                    print('Total data points: %s' % len(data_scan[dev_to_scan][d]))






    def set_value_to_device(self, dev_name, value):
        """ Sets the value of the device. If it is an analog output, it takes just one value.
        If it is a device connected through serial, etc. it takes a dictionary.
        :param dev_name: name of the device to set the output
        :param value: value or dict of values to set the device to
        """
        dev = self.devices[dev_name]
        # If it is an analog channel
        if dev.properties['connection']['type'] == 'daq':
            daq = self.devices[dev.properties['connection']['device']]
            conditions = {
                'dev': dev,
                'value': value
            }
            daq.driver.analog_output(conditions)
        else:
            self.devices[dev.dev.properties['name']].apply_values(values)






if __name__ == "__main__":
    config_experiment = "config/measurement.yml"
    experiment_dict = from_yaml_to_dict(config_experiment)
    experiment = measurement(experiment_dict)
    experiment.initialize_devices()