# -*- coding: utf-8 -*-
"""
    Measurement class
    =================

    The measurement class is a general idea in which to lay out the logic of the experiment to perform. There are not
    predefined boundaries. Several methods guide the step-by-step process for performing an experiment; they should be
    ideally defined before starting to write. This guives the user a clearer idea of what needs to be developed, step
    by step. For example, in order to perform a 2D scan of the laser and an extra device, the following methods have to
    be defined:

    - `load_devices` reads the file established in the init property of the dictionary
    - `initialize_devices` iterates through all the devices and initializes them provided they have a driver
    - `connect_all_devices_to_daq` checks which devices are connected to a DAQ and appends them

    .. warning:: In the Experimentor program this is now done radically different.

    - `synch_shutter` was added by Karindra in order to cycle through the shutter and guarantee that Digou high => shutter open
    -
    - `setup_scan` prepares the laser and the ADQ for the measurement, but it doesn't trigger it.
    - `do_scan` actually is responsible for performing the 2D scan. It has a for loop that blocks the execution.
    - `do_line_scan` does a 1D wavelength scan, it runs inside the loop of the `do_scan`
    - `set_value_to_device` sets a particular value to a specific device, considering how it is connected, etc. It should work both with devices connected to a DAQ and to devices connected directly to the computer.

    .. todo:: The class does not leverage the capabilities of Qt for threading and emitting signals
    .. todo:: data is read but not stored within the class; maybe it should be better to have it built-in
    .. todo:: There is no method for saving; it was introduced in the GUI. Maibe it would make it a bit more robust.


    Having a dictionary

"""
import numpy as np
from time import sleep
import time
from lantz import Q_
from pharos.model.lib.general_functions import from_yaml_to_devices, from_yaml_to_dict
from pharos.config import config
import os

os.environ['PATH'] = os.environ['PATH'] + ';' + 'C:\\Program Files (x86)\\Thorlabs\\Kinesis'


class Measurement(object):
    def __init__(self, measure):
        """Measurement class that will hold all the information regarding the experiment being performed.
        The main idea is that a dictionary constructed from a yaml file is passed as argument. Each
        main key of the dictionary will be available straight in the class as `self.main_key`. See the lines that read::

            for d in measure:
                setattr(self, d, measure[d])

        :param measure: a dictionary with the necessary steps
        """
        self.measure = measure  # Dictionary of the measurement steps
        self.devices = {}  # Dictionary holding all the devices
        self.output_devices = [] # List of devices with output capabilities
        self.daqs = {}  # Dictionary that holds for each daq the inputs and outputs.
        self.rotation_stages = [] # If there are rotation stages present, they will show up in this list.
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
            if 'outputs' in dev.properties:
                self.output_devices.append(dev)
            print('Added %s to the experiment' % dev)
            if dev.properties['type'] == "Rotation Stage":
                self.rotation_stages.append(dev.properties['name'])

    def initialize_devices(self):
        """ Initializes the devices first by loading the driver,
        then by applying the default values if they are present.
        :return:
        """
        for k in self.devices:
            dev = self.devices[k]
            print('Starting %s' % dev.properties['name'])
            dev.initialize_driver()
            #    print('Error initializing %s' % dev.properties['name'])
            if 'defaults' in dev.properties:
                defaults_file = dev.properties['defaults']
                defaults = from_yaml_to_dict(defaults_file)[dev.properties['name']]
                dev.apply_values(defaults)
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
            if 'connection' in dev.properties:
                if 'device' in dev.properties['connection']:
                    connected_to = dev.properties['connection']['device']
                    mode = dev.properties['mode']
                    self.daqs[connected_to][mode].append(dev)
                    print('Appended %s to %s' % (dev, connected_to))

    def connect_monitor_devices_to_daq(self):
        """ Connects only the devices to be monitored to the appropriate daq
        :return:
        """
        scan = self.measure['scan']
        devices_to_monitor = scan['detectors']

        # Clear the DAQS just in case is a second scan running
        for d in self.daqs:
            self.daqs[d]['monitor'] = []

        for d in devices_to_monitor:
            dev = self.devices[d]
            self.daqs[dev.properties['connection']['device']]['monitor'].append(dev)

    def sync_shutter(self):
        """ Opens and closes the shutter to be sure the digout high means shutter open."""
        shutter = self.scan['shutter']
        ni_daq = self.devices['NI-DAQ']
        ni_daq.driver.digital_output(shutter['port'], False)
        time.sleep(0.2)
        ni_daq.driver.digital_output(shutter['port'], True)
        time.sleep(0.2)
        ni_daq.driver.digital_output(shutter['port'], False)

    def setup_scan(self):
        """ Prepares the scan by setting all the parameters to the DAQs and laser.
        THIS METHOD WORKS WITH VERY SPECIFIC SETUP CONDITIONS!
        :return:
        """
        scan = self.scan
        # First setup the laser
        laser_params = scan['laser']['params']
        laser = self.devices[scan['laser']['name']]
        if 'wavelength_sweeps' not in laser_params:
            laser_params['wavelength_sweeps'] = 1  # This to avoid conflicts in downstream code.
        elif laser_params['wavelength_sweeps'] == 0:
            laser_params['wavelength_sweeps'] = 1  # This to avoid conflicts in downstream code.
        
        laser_params['wavelength'] = laser_params['start_wavelength']

        num_points = (laser_params['stop_wavelength'] - laser_params['start_wavelength']) / laser_params['interval_trigger'] * laser_params['wavelength_sweeps']
        num_points = int(num_points.m_as(''))+1

        # Some NI DAQs misbehave with odd number of data points.
        if num_points % 2 != 0:
            laser_params['stop_wavelength'] += laser_params['interval_trigger']
            num_points += 1

        self.scan['laser']['params'] = laser_params
        laser.apply_values(laser_params)

        # Clear the array to start afresh
        for d in self.daqs:
            self.daqs[d]['monitor'] = []

        # Lets see what happens with the devices to monitor
        devices_to_monitor = scan['detectors']

        for dev_name in devices_to_monitor:
            dev = self.devices[dev_name]
            self.daqs[dev.properties['connection']['device']]['monitor'].append(dev)
            print('Appending {} to {}'.format(dev_name, dev.properties['connection']['device']))

        dev_to_scan = scan['axis']['device']['name']
        output_to_scan = scan['axis']['device']['property']
        if dev_to_scan != 'time':
            dev_range = scan['axis']['device']['range']
            start = Q_(dev_range[0])
            stop = Q_(dev_range[1])
            step = Q_(dev_range[2])
            num_points_dev = int(((stop-start)/step).m_as(''))+1
        else:
            dev_range = scan['axis']['device']['range']
            start = 1
            stop = dev_range[1]
            num_points_dev = stop
        # This is temporal accuracy for the DAQ.
        print('Number of points device: {}'.format(num_points_dev))
        print('Number of points scan: {}'.format(num_points))
        accuracy = laser.params['interval_trigger'] / laser.params['wavelength_speed']

        conditions = {
            'accuracy': accuracy,
            'points': num_points*num_points_dev,
        }
        self.scan['total_points'] = conditions['points']
        # Then setup the DAQs
        for d in self.daqs:
            daq = self.daqs[d]  # Get the DAQ from the dictionary of daqs.
            daq_driver = self.devices[d]  # Gets the link to the DAQ
            
            if len(daq['monitor']) > 0:
                print('DAQ: %s' % d) 
                devs_to_monitor = daq['monitor']  # daqs dictionary groups the channels by daq to which they are plugged
                print('Devs to monitor:')
                print(devs_to_monitor)
                conditions['points'] *= len(daq['monitor'])
                conditions['devices'] = devs_to_monitor
                conditions['trigger'] = daq_driver.properties['trigger']
                conditions['trigger_source'] = daq_driver.properties['trigger_source']
                print('Trigger source {}'.format(conditions['trigger_source']))
                conditions['sampling'] = 'continuous'
                daq['monitor_task'] = daq_driver.driver.analog_input_setup(conditions)
                self.daqs[d] = daq  # Store it back to the class variable
                print('Monitor Task: {}'.format(self.daqs[d]['monitor_task']))
                if not daq_driver.driver.is_task_complete(daq['monitor_task']):
                    daq_driver.stop_task(daq['monitor_task'])
                daq_driver.driver.trigger_analog(None)

        approx_time_to_scan = (laser.params['stop_wavelength'] - laser.params['start_wavelength']) / laser.params['wavelength_speed']

        self.measure['scan']['approx_time_to_scan'] = approx_time_to_scan

    def do_line_scan(self):
        """ Does the wavelength scan.
        After a line scan, the different devices should be increased by 1, etc."""
        scan = self.scan
        laser = self.devices[scan['laser']['name']]
        shutter = self.scan['shutter']
        ni_daq = self.devices['NI-DAQ']
        ni_daq.driver.digital_output(shutter['port'], False)
        if not isinstance(shutter['delay'], Q_):
            delay = Q_(shutter['delay'])
        else:
            delay = shutter['delay']
        delay = delay.m_as('s')
        time.sleep(delay)
        ni_daq.driver.digital_output(shutter['port'], True)
        laser.driver.execute_sweep()
        approx_time_to_scan = (laser.params['stop_wavelength'] - laser.params['start_wavelength']) / laser.params['wavelength_speed']*laser.params['wavelength_sweeps']

        while laser.driver.sweep_condition != 'Stop':
            sleep(approx_time_to_scan.m/config.monitor_read_scan)
        ni_daq.driver.digital_output(shutter['port'], False)

        return True

    def do_scan(self):
        """ Does the scan considering that everything else was already set up.
        """
        scan = self.scan
        laser = self.devices[scan['laser']['name']]
        dev_to_scan = scan['axis']['device']['name']
        output = scan['axis']['device']['property']
        approx_time_to_scan = (laser.params['stop_wavelength']-laser.params['start_wavelength'])/laser.params['wavelength_speed']
        # Scan the laser and the values of the given device
        if dev_to_scan != 'time':
            dev_range = scan['axis']['device']['range']
            start = Q_(dev_range[0])
            units = start.u
            stop = Q_(dev_range[1])
            step = Q_(dev_range[2])
            
            num_points_dev = ((stop-start)/step).to('')
        else:
            dev_range = scan['axis']['device']['range']
            start = 1
            stop = dev_range[1]
            num_points_dev = stop

        num_points_dev += 1  # So the last bit of information is true.

        for value in np.linspace(start, stop, num_points_dev, endpoint=True):
            if dev_to_scan != 'time':
                self.set_value_to_device(dev_to_scan, {output: value * units})
                dev = self.devices[dev_to_scan]
                time.sleep(0.1)
                while not dev.driver.finished_moving:
                    time.sleep(0.2)

            self.do_line_scan()
            
        return True

    def set_value_to_device(self, dev_name, value):
        """ Sets the value of the device. If it is an analog output, it takes just one value.
        If it is a device connected through serial, etc. it takes a dictionary.
        :param dev_name: name of the device to set the output
        :param value: value or dict of values to set the device to
        """
        dev = self.devices[dev_name]
        # If it is an analog channel
        if 'model' in dev.properties:
            if dev.properties['model'] == 'ni':
                daq = self.devices[dev.properties['connection']['device']]
                conditions = {
                    'dev': dev,
                    'value': value
                }
                daq.driver.analog_output_dc(conditions)
        else:
            dev.apply_values(value)

    def setup_continuous_scans(self, monitor=None):
        """ Sets up scans that continuously start. This is useful for monitoring a signal over time.
        In principle it is similar to doing a 2D scan with time as a parameter.
        """
        if monitor is None:
            monitor = self.monitor
        else:
            self.monitor = monitor

        # Lets grab the laser
        laser = self.devices[monitor['laser']['name']]
        if 'wavelength_sweeps' not in monitor['laser']['params']:
            monitor['laser']['params']['wavelength_sweeps'] = 0  # This will generate the laser to sweep always.

        # Clear the array to start afresh
        for d in self.daqs:
            self.daqs[d]['monitor'] = []

        # Lets see what happens with the devices to monitor
        devices_to_monitor = monitor['detectors']

        for dev in devices_to_monitor:
            self.daqs[dev.properties['connection']['device']]['monitor'].append(dev)

        # Lets calculate the conditions of the scan
        num_points = int(
            (self.monitor['laser']['params']['stop_wavelength'] - self.monitor['laser']['params']['start_wavelength'])
            / self.monitor['laser']['params']['interval_trigger'])+1

        # Some DAQ cards behave strangely when dealing with even/odd number of points.
        # Using an even number of data points makes it behave correctly 'always'
        if num_points % 2 != 0:
            #  Increase the stop wavelength in one step in order to have an extra data point
            self.monitor['laser']['params']['stop_wavelength'] += self.monitor['laser']['params']['interval_trigger']
            num_points += 1

        accuracy = self.monitor['laser']['params']['interval_trigger'] / self.monitor['laser']['params']['wavelength_speed']

        approx_time_to_scan = (self.monitor['laser']['params']['stop_wavelength'] - self.monitor['laser']['params']['start_wavelength']) / self.monitor['laser']['params'][
            'wavelength_speed']

        laser.apply_values(self.monitor['laser']['params'])
        self.measure['monitor']['approx_time_to_scan'] = approx_time_to_scan
        
        wl_sweeps = int(monitor['laser']['params']['wavelength_sweeps'])
        if wl_sweeps > 0:
            num_points = num_points * wl_sweeps
            if monitor['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                num_points = num_points*2
            sampling = 'continuous'
        else:
            sampling = 'continuous'
        conditions = {
            'accuracy': accuracy,
            'points': num_points
        }
        # Then setup the ADQs
        for d in self.daqs:
            daq = self.daqs[d]  # Get the DAQ from the dictionary of daqs.
            daq_driver = self.devices[d]  # Gets the link to the DAQ
            if len(daq['monitor']) > 0:
                print('DAQ: %s' % d)
                devs_to_monitor = daq['monitor']  # daqs dictionary groups the channels by daq to which they are plugged
                print('Devs to monitor:')
                print(devs_to_monitor)
                conditions['devices'] = devs_to_monitor
                if 'trigger' not in self.monitor['daq']:
                    raise Exception('A trigger has to be specified in the daq section of the monitor')
                conditions['trigger'] = self.monitor['daq']['trigger']
                print('Trigger: %s' % conditions['trigger'])
                if conditions['trigger'] == 'external':
                    # It should specify also which port to use
                    conditions['trigger_source'] = self.monitor['daq']['trigger_source']
                    print('Trigger source: %s' % conditions['trigger_source'])
                elif conditions['trigger'] == 'internal':
                    if self.monitor['daq']['trigger_source'] is not None:
                        raise Warning('Specifying trigger even if set to Internal.')
                else:
                    raise Exception('Trigger not recognized. Check the config. Only external or internal can be used.')

                if 'start_trigger' in self.monitor['daq']:
                    if self.monitor['daq']['start_trigger'] is not None:
                        conditions['start_source'] = self.monitor['daq']['start_source']
                        conditions['start_mode'] = 'digital'
                    else:
                        conditions['start_mode'] = 'software'

                conditions['sampling'] = sampling
                daq['monitor_task'] = daq_driver.driver.analog_input_setup(conditions)
                self.daqs[d] = daq  # Store it back to the class variable
                print('Task number: %s' % self.daqs[d]['monitor_task'])

    def start_continuous_scans(self):
        """Starts the laser, and triggers the daqs. It assumes setup_continuous_scans was already called."""
        monitor = self.monitor
        laser = self.devices[monitor['laser']['name']]
        
        for d in self.daqs:
            daq = self.daqs[d]
            daq_driver = self.devices[d].driver
            #daq_driver.reset_device()
            if len(daq['monitor'])>0:
                devs_to_monitor = daq['monitor']  # daqs dictionary groups the channels by daq to which they are plugged             
                if daq_driver.is_task_complete(daq['monitor_task']):
                    daq_driver.trigger_analog(daq['monitor_task'])
        laser.driver.execute_sweep()
        #sleep(1)

    def read_scans(self, points=0):
        """ Reads the data from the DAQ. It has 3 modes of operation:
            - points>0: reads that number of points from the daq, or timeouts if not enough available.
            - points=0: splits the points and the buffer, i.e. this is idea when acquiring more than 1 channel, since points and buffer have different meanings for NI.
            - points<0: reads all the available points in the DAQ.
        """
        
        data = {}
        for d in self.daqs:
            daq = self.daqs[d]
            daq_driver = self.devices[d]
            if len(daq['monitor']) > 0:
                if points == 0:
                    total_points = self.scan['total_points']
                    conditions = {'points': total_points}
                    conditions['buffer_length'] = total_points*len(daq['monitor'])
                else:
                    conditions = {'points': points}
                vv, dd = daq_driver.driver.read_analog(self.daqs[d]['monitor_task'], conditions)
                dd = dd[:vv*len(daq['monitor'])]
                dd = np.reshape(dd, (len(daq['monitor']), int(vv)))
                for i in range(len(daq['monitor'])):
                    dev = daq['monitor'][i]
                    data[dev.properties['name']] = dd[i,:]
        return data
        
    def read_continuous_scans(self):
        conditions = {'points': -1} # To read all the points available
        data = {}
        for d in self.daqs:
            daq = self.daqs[d]
            daq_driver = self.devices[d]
            if len(daq['monitor']) > 0:
                vv, dd = daq_driver.driver.read_analog(daq['monitor_task'], conditions)
                dd = dd[:vv*len(daq['monitor'])]
                dd = np.reshape(dd, (len(daq['monitor']), int(vv)))
                for i in range(len(daq['monitor'])):
                    dev = daq['monitor'][i]
                    data[dev.properties['name']] = dd[i,:]
        return data

    def stop_laser(self):
        laser = self.devices[self.scan['laser']['name']].driver
        laser.pause_sweep()
        laser.stop_sweep()

    def stop_scan(self):
        scan = self.scan
        self.stop_laser()
        ni_daq = self.devices['NI-DAQ']
        shutter = self.scan['shutter']
        ni_daq.driver.digital_output(shutter['port'], False)
        for d in self.daqs:
            daq = self.daqs[d]
            if len(daq['monitor']) > 0:
                daq_driver = self.devices[d].driver
                if not daq_driver.is_task_complete(daq['monitor_task']):
                    daq_driver.stop_task(daq['monitor_task'])
                    daq_driver.clear_task(daq['monitor_task'])

    def read_last_values(self):
        conditions = {'points': -1} # To read all the points available
        data = {}
        for d in self.daqs:
            daq = self.daqs[d]
            daq_driver = self.devices[d]
            if len(daq['monitor']) > 0:
                vv, dd = daq_driver.driver.read_analog(daq['monitor_task'], conditions)
                t1 = time.time()
                dd = dd[:vv*len(daq['monitor'])]
                dd = np.reshape(dd, (len(daq['monitor']), int(vv)))
                for i in range(len(daq['monitor'])):
                    dev = daq['monitor'][i]
                    data[dev.properties['name']] = dd[i,:]
        print('Reading last values')
        return data
            
    def stop_continuous_scans(self):
        monitor = self.monitor
        laser = self.devices[monitor['laser']['name']].driver
        laser.pause_sweep()
        laser.stop_sweep()
        for d in self.daqs:
            daq = self.daqs[d]
            if len(daq['monitor']) > 0:
                daq_driver = self.devices[d].driver
                if not daq_driver.is_task_complete(daq['monitor_task']):
                    daq_driver.stop_task(daq['monitor_task'])
                    daq_driver.clear_task(daq['monitor_task'])

    def pause_continuous_scans(self):
        monitor = self.monitor
        laser = self.devices[monitor['laser']['name']].driver
        laser.pause_sweep()

    def resume_continuous_scans(self):
        monitor = self.monitor
        laser = self.devices[monitor['laser']['name']].driver
        laser.resume_sweep()

    def open_shutter(self):
        shutter = self.scan['shutter']
        ni_daq = self.devices['NI-DAQ']
        ni_daq.driver.digital_output(shutter['port'], True)

    def close_shutter(self):
        shutter = self.scan['shutter']
        ni_daq = self.devices['NI-DAQ']
        ni_daq.driver.digital_output(shutter['port'], False)


if __name__ == "__main__":
    config_experiment = "config/measurement.yml"
    experiment_dict = from_yaml_to_dict(config_experiment)
    experiment = Measurement(experiment_dict)