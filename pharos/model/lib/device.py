# -*- coding: utf-8 -*-
"""
    Device class
    ============
    In the Pharos context, everything that is part of an experiment is a device. The National Instruments card is a
    device, the photodiode is a device, etc. Therefore, a general class called Device is handy for defining some common
    behavior to all devices.

    Devices are created with a dictionary of properties passed as only argument, and will be store as a property called
    `properties`. This shouldn't change over time, and therefore allows to user to go back to the pristine status of the
    device. On the other hand, the property `params` stores a dictionary of the latest values passed to a given device.
    In order to check whether a particular parameter was altered, it is sufficient to compare it with the properties.

    .. warning:: The experimentor package makes the properties and the params behave in different ways, for example by
    making them write-only if needed.

    The most important methods available in a device are `initialize_driver` and `apply_values`. The first checks if a
    driver is part of the properties and initializes it according to the connection type. It is of paramount importance
    to note that this is heavily dependant on how `Lantz` initializes drivers. The only exception is the `daq` type of
    connection, that loads the specific module and passes the port as argument.

    .. todo:: If a user needs to specify a driver that takes more arguments, or is of a different kind, the place to
    look at is the `initialize_driver` method. Appropriate conditionals at this stage can take care of a great deal of
    different scenarios.

    `apply_values` takes a dictionary with the structure 'property' => 'value' and directly applies it to the driver.
    Again this is assuming the use of Lantz drivers, where doing things like laser.wavelength = 1200*Q_('nm') makes sense.

    .. todo:: In principle not all drivers behave in the same way. Interfacing devices with a model rather than with a
    lower level driver may be a good idea.

    .. todo:: It may be handy to expand the toolbox of devices. For example, being able to do a ramp.


    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""

import importlib
from lantz import Q_


class device(object):
    """ Device object that takes as only argument a dictionary of properties. There are no required fields a-priory,
    except the method `initialize_driver` is used. In this case there should be a driver and a connection specified.

    :param properties: Dictionary with all the properties of the device. Normally it is generated from a YAML file.

    .. codeauthor:: Aquiles Carattino <aquiles@uetke.com>

    """
    def __init__(self, properties):
        self.properties = properties
        self.driver = None
        self.params = {}

    def add_driver(self, driver):
        """ Adds the driver of the device. It has to be initialized()

        :param driver: driver of any class.
        """
        self.driver = driver

    def initialize_driver(self):
        """ Initializes the driver of the given device. If no driver is specified (for example when dealing with a device
        connected to a ADQ card, nothing happens.
        'driver' and 'connection' should be available in the properties. The driver is initialized according to the Lantz
        way of doing it. Except if the ['connection']['type'] is 'daq', in which case the 'port' is passed as an argument
        to the initialization. This is how the NI class works, and can be used also for non DAQ devices, such as the
        rotation stage that takes the serial number as argument.

        .. todo:: Nothing prevents a user from interacting directly with the driver without passing through the class
        Device. This may give rise to unwanted programming patterns.

        """
        if 'driver' in self.properties:
            d = self.properties['driver'].split('/')
            driver_class = getattr(importlib.import_module(d[0]), d[1])
            if 'connection' in self.properties:
                connection_type = self.properties['connection']['type']
                if connection_type == 'GPIB':
                    # Assume it is a lantz driver
                    self.driver = driver_class.via_gpib(self.properties['connection']['port'])
                    self.driver.initialize()
                elif connection_type == 'USB':
                    # Assume it is a lantz driver
                    self.driver = driver_class.via_usb()
                    self.driver.initialize()
                    raise Warning('This was never tested!')
                elif connection_type == 'serial':
                    # Assume it is a lantz driver
                    self.driver = driver_class.via_serial(self.properties['connection']['port'])
                    self.driver.initialize()
                    raise Warning('This was never tested!')
                elif connection_type == 'daq':
                    self.driver = driver_class(self.properties['connection']['port'])

    def apply_values(self, values):
        """ Iterates over all values of a dictionary and sets the values of the driver to it. The driver has to be set
        and has to be able to handle a `setattr(driver, key, value)` command. Lantz drivers in which a Feat with a
        setter was defined work out of the box.
        For other devices a workaround should be found.

        :param values: a dictionary of parameters and desired values for those parameters
        """
        if isinstance(values, dict):
            for k in values:
                try:
                    # Tries to convert to proper units, if it fails it uses the value as is
                    value = Q_(values[k])
                except:
                    value = values[k]
                print('Setting %s to %s'%(k, value))
                try:
                    setattr(self.driver, k, value)
                except:
                    print('Problem setting %s in %s' % (k, self))
                self.params[k] = value
        else:
            raise Exception('Drivers can only update dictionaries')

    def get_params(self):
        """ Work in progress, already implemented in the Experimentor. A buffer function that allows to have read-only
        parameters provided that the decorator `@property` is used.

        :return: Dictionary of parameters used for initializing the class.
        """
        return self.params

    def __str__(self):
        if 'name' in self.properties:
            return self.properties['name']
        else:
            return "Device with no name"

if __name__ == "__main__":
    from pharos.model.lib.general_functions import from_yaml_to_devices

    d = from_yaml_to_devices('../../config/devices.yml', name='dummy daq')[0]
    d.initialize_driver()
    print(d)