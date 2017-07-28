# MODELS #
The models are a layer of abstraction for the devices. A way of realizing the plug-and-play dream. **But not only that**. Starting with Pharos v0.1, models also hold special classes for defining _experiments_ and _devices_.

## Experiments ## 
    experiment.measurement
Is one of the examples on how an experiment is set-up. The `Measurement` class will deal with each of the steps defined in the `config/measurement.yml` file. The idea is that different methods of the class will take care of different stages of the measurement. In this case, one method will be in charge of loading the devices, one will be in charge of initializing them, setting up a scan, etc. 

Splitting it into different methods allows a greater flexibility at the time of reusing code and building a GUI. The YML file is read as a dictionary and passed to the `Measurement` class. Each key in the dictionary is transformed to a property of the class. In this way, one can have `measurement.init` available. The parameters of each step can be overridden, and therefore they are able to handle user interaction at runtime, a fundamental property for GUI development.

## Devices ## 
    lib.devices
The devices class holds some methods for interfacing with different kind of devices. It is still work in progress, but it allows to load a driver, initialize it and set values to different parameters. In principle it can also check if the device is a DAQ, a sensor plugged to a DAQ or an independent device connected through serial, etc.

--------

## Logic for designing a new experiment/GUI/etc ## 
The first step is to think about the experiment to be done; what are the devices that are going to be needed, what are the steps of the measurement, etc. This has to be written in the YAML file in the config folder. Following the example of `example_confocal` is a good idea. 

To illustrate the creation process, the steps would be as follows (of course very much simplified.) Whatever appears in between `[]` refers to sections in the YAML file.

 - The `[init]` section holds the information of the devices (maybe linking to an external file)
    - This section can also provide default values for the devices
 - One or several functions defined in the model will take care of what is given in init. A function may  just read the configuration files of the devices, a different function can set the defaults to each device, etc.
 - The `[scan]` section will hold the information of an actual confocal scan. The first thing one realizes is that a confocal scan needs some `[axis]`, meaning what is going to be scanned and `[detectors]`, i.e. what signals are going to be recorded while scanning.
 - In the `Measurement` model, a set of functions will prepare the DAQ cards for the scan, a function will trigger the scan and a function will read the data. 
 - It is possible to realize that defining the axis is not enough, each axis need ranges and a speed. Going back to the YAML file it is possible to add extra parameters under each `[axis]`.
 - A `[finalize]` method ensures that the setup is left in a state useful for the next measurement, for example by closing shutters, switching off a device, etc. 
 
In this process many things will be encountered for which there is no trivial solution. For example, if a user needs to synchronize the acquisition with an external trigger, the `model.daq.ni` will not provide support. Therefore a new method, or an improvement of the available methods has to be done. Remember to maintain backwards compatibility. A good idea is to enclose new conditions with an `if` that ensures that older code will still run.
 
## TODO ##
- The measurement class is not general; new experiments can't rely on subclassing as it is. 
    - [ ] Make a base class for measurements defining common methods, properties and decorators.
    - [ ] Subclass the already present classes from the general one. 
- The devices are poorly implemented and are not as flexible as they should be. Difference between device and sensor is crucial. So far, both a DAQ and a photodiode plugged to it are considered devices. This comes from an older design in which there were _only_ devices plugged to _one_ daq.
    - [ ] Following the TODO from `config`, devices should be those who are able to `set` or `get` a value to the real world.
    - [ ] Devices should have methods for getting and setting properties, maybe defined in a YML file (only those properties relevant for the experiment).
    - [ ] A new class, `sensors` has to be developed, in which for example the _port_ and the _limits_ are specified.
    - [ ] Care has to be taken in not duplicating the work done at other packages, such as [Lantz](https://github.com/LabPy/lantz), or [Instrumental](https://github.com/mabuchilab/Instrumental).