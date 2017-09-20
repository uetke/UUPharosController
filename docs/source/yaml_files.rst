.. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>

Understanding the YAML files
============================
The Pharos controller needs YAML files to configure some basic parameters. The YAML files are not just a whim, they make very explicit the different variables available to someone programming and therefore be used as a quick reference.

They also make possible quick changes in some default values, for example if a new photodiode is connected to the NI card, the laser changes from a GPIB connection to an USB connection, etc. Understanding the layout of these files is important but bear in mind that they are always read by a python program, that you are free to modify at your own discretion.

Devices.yml
~~~~~~~~~~~
The Pharos Controller was built upon an outdated idea of how to define devices. Basically everything in a setup is a
device. The main difference is that some devices are connected to other instead of to a computer. Therefore, the program
uses only one devices.yml file.

A general device such as a laser can be defined like this:

.. code-block:: yaml

    TSL-710:
      type: scan laser
      name: Santec Laser
      driver: controller.santec.tsl710/tsl710
      connection:
        type: GPIB
        port: 1
      defaults: config/devices_defaults.yml

Remember that per-se, yaml files do not do anything. They have to be interpreted later by python code. The main key, `TSL-710` identifies the device and has to be unique, however is not use in downstream code. What is used is the name, that also hase to be unique (and can be the same as the main key). The driver specifies which Python module has to be used to communicate with the device. That particular line would translate to Python code like this::

    from controller.santec.tsl710 import tsl710

.. todo::

    The code should rely on models that have standardized behavior, more than directly on drivers.

The `connection` block will be interpreted later on, and will be fed to the driver to make a connection. Knowing the type of communication the device has (GPIB, USB, Serial, etc.) and the port to which it is connected, is a responsibility of the user.

A daq card, such as an NI card can be defined as follows:

.. code-block:: yaml

    NI-DAQ:
      name: NI-DAQ
      type: daq
      model: ni
      number: 2
      driver: pharos.model.daq.ni/ni
      connection:
        type: daq
        port: 2
      trigger: external
      trigger_source: PFI0
Again, the name is the important parameter here. Moreover the last block specifies the kind of trigger we want to use for the DAQ.

.. todo:: Specifying the trigger when defining the DAQ is not a good idea, since in the same experiment there can be different needs. Monitoring a signal while aligning can be done without an external trigger. Being that the case, it would have made the code much more reusable if the trigger is defined elsewhere.

A photodiode connected to the ADQ can be defined like so:

.. code-block:: yaml

    PhotoDiode2:
      name: Photodiode 2
      port: 2
      type: analog
      mode: input
      description: Forward Intensity
      calibration:
        units: V
        slope: 1
        offset: 0
      limits:
        min: -2.5
        max: 2.5
      connection:
        type: daq
        device: NI-DAQ
Everything is more or less self explanatory. The calibration refers to how to convert from Volts to the units of the device. For example a piezo stage receives voltage, but it is transduced into distance. A thermocouple outputs voltage, but has a meaning of temperature, etc. The units here can be anything interpreted by the Pint module. The limits are the limits in the units given by the calibration. Limits are mandatory when dealing with NI cards, since it automatically chooses the best gain to optimize the digitalization range.

Lastly, the connection block explicitly states to which device it is connected.

.. warning:: This structure is cumbersome and was already superseded in the Experimentor program. If you are going to develop something new, I strongly suggest that you check that other program.

Measurement.yml
~~~~~~~~~~~~~~~
The measurement.yml file defines the basic structure of an experiment. It defines what parameters are needed, what detectors are recorded, etc. Whatever you add in here will be later available in the experiment class. Each main key of the file should be different steps of your experiment. For example::

    init:
      devices: 'config/devices.yml'
When initializing, the only important thing is to know where the file with the definition of the devices is. In the initialization step, we can use the information used in the property `devices` to initialize the appropriate drivers, etc.

Once we have our devices configured, we would like to do a scan. We call this a monitor, because in principle the scan can be repeating itself over and over:

.. code-block:: yaml

    monitor:
      laser:
        name: Santec Laser
        params:
          start_wavelength: 1491 nm
          stop_wavelength:  1510 nm
          wavelength_speed:  10 nm/s
          interval_trigger: 0.01 nm
          sweep_mode: ContOne
          wavelength_sweeps: 1
      detectors:
      - Photodiode Test
      - Photodiode 2
You see now that we define the laser we want to scan (in case there is more than one), and we refer to it by its name. We define some parameters and some detectors.

.. note:: Because of how the parser of the YAML file works, params is going to be a dictionary, while detectors is going to be a list.

If we want to fancy things up a bit, for example with 2-D scans instead of just 1D, we have to define which axis are we scanning. This axis should be another device and should have a range. If the device is not connected to a DAQ, we should also specify which property we would like to scan. We can do it like so:

.. code-block:: yaml

    scan:
      laser:
        name: Santec Laser
        params:
          start_wavelength: 1492 nm
          stop_wavelength:  1548 nm
          wavelength_speed:  50 nm/s
          interval_trigger: 0.01 nm
          sweep_mode: ContOne
          wavelength_sweeps: 1
      axis:
        device:
          name: Rotation 1
          range: [35deg, 55deg, 1deg]
          property: position
      detectors:
        - Photodiode Test
        - Photodiode 2
Imagine now that later on, you decide you need to have a shutter controlling a secondary laser. And you need that shutter to be closed after a scan, and to have a small delay before a new line scan starts. At least in what the configuration needs, you should only add these three lines:

.. code-block:: yaml

      shutter:
        port: PFI2
        delay: 100ms
And of course we should also include what to do once the experiment is over. For example we want to close the shutter of the laser, but not switch it off:

.. code-block:: yaml

    finish:
      TSL-10:
        shutter: False
