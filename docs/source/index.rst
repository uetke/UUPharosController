.. Pharos Controller documentation master file, created by
   sphinx-quickstart on Tue Aug 29 13:51:54 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pharos Controller's documentation!
=============================================
The Pharos Controller can be installed as any other Python package by using the setup.py file provided. It can also be
directly downloaded and run from within the folder. There are two main starting points: `start_gui` and
`start_measurement`. The first starts a Window that allows to control the laser and perform scans, while the second is
a simple example of how the same program can be utilized without user interfaces.

This guide will help you understand the logic behind the program and will quickly guide you on how to add new features or
change the logic of the measurement. If you need help, you can always find more information on Github and on Readthedocs.

General Structure
~~~~~~~~~~~~~~~~~
The program can be split into different layers. For the time being I will disregard the GUI part of the software,
focusing only on the functioning logic behind it. The general principle of functioning is that a user should be able to
plan the experiment ahead. He should be aware of what sensors and actuators are available, their ranges, how they are
interconnected. For example the Pharos setup is very specific in the way signals are acquired; the NI card digitalizes a
channel only when it receives a trigger from the scanning laser. In turn, the laser can be programmed to issue a trigger
at very specific wavelengths, and thus the experiment itself consists on acquiring spectra.

The general principle of operation would be: first defining some configuration files for the devices and the experiment.
These files are then read and interpreted by different Python objects. One of this objects is actually an `Experiment`
object, that will hold all the logic, for example first preparing the acquisition card, then triggering the
scan of the laser. Then the user can trigger different actions by calling different methods. The same structure can work
for any kind of experiment and therefore it was brought as a separate package called Experimentor, that you can also find
on Github.

A quick walk-through
~~~~~~~~~~~~~~~~~~~~
The first step is to create some yaml files with definitions. For example, one can start with
the file `devices.yml`, in which every device is going to be specified; this means establishing to which port of the daq
card a sensors is plugged, to which GPIB port of the computer the laser is connected, etc. The we define an
`experiment.yml` file, in which we put every step of the experiment, from the initialization, to the scan and the
finalization. Yaml files are quickly associated with dictionaries in Python and therefore they are also a useful resource
when programming.

Then we need to write the experiment class. In this class we are going to load the devices and store them as a property.
We are going to initialize them, i.e. we are going to start the communication with them. We are also going to load the
experiment config file and we will generate methods to set up every step of a measurement. We have a `setup_scan` method
as well as a `do_scan` method. I suggest you check them out to understand quickly what they are doing. The class is stored
in `pharos.model.experiment`. You can also see a second example on how to build a confocal microscope with this logic.

Once everything is set up, we write our last script, the `start_measurement`. This script will call the different methods
defined in the experiment class, for example, loading the devices, performing a scan, changing the parameters and performing
a new scan. Something important to note is that after loading the YAML file to the experiment class, every property can be
changed from outside the class. So, if we defined a laser sweep speed in the yaml file, we can easily alter it from outside::

    experiment.laser.params['sweep_speed'] = New_Value

And the same is valid for all the different properties that are set through the Yaml file. The Experimentor project has
several improvements in this regard, making it explicit which properties can be set and which properties can only be read.

With this logic in mind, a GUI is nothing but a way of passing values to the experiment class and a trigger of specific
methods.




.. toctree::
   :maxdepth: 2
   :caption: Contents:

   yaml_files
   devices
   NI_Model
   experiment_class
