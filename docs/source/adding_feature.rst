Adding a new feature
====================
Adding a new feature to the software is as important as being able to add a new device to the setup. Science changes,
experiments change, and software should follow that behavior. In this page I will guide you step by step on how to add
a shutter to the experiment. The shutter will close right after a line scan is done and will stay closed for a fixed time
before a new scan starts. This prevents the sample from overheating due to the laser itself.

Identifying the hardware needs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The first step, even if redundant, is where most users fail. Identifying the need means understanding what do you want to do and how do you plan to do it. In the case of a `Thorlabs Shutter <https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_ID=927>`_, you can see that there are plenty of different configurations. Let's assume you have the shutter SH1, and the cube for controlling it KSC101. The cube can be controlled from the computer via an USB connection; however this would imply finding drivers for it, etc. It can also be controlled via a TTL signal coming from a DAQ. For simplicity, in this example we are going to use the TTL signal.

.. warning:: It is **very** important that you read the manual and that you understand how the device operates. Some things are trivial (for example the cube has a button called enable), but some are not. Depending on the version of the cube you have, the behaviour of the shutter will be different. For example it can close automatically even if there is no TTL signal indicating to do so.

Identifying the software needs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The next step is to identify what has to be done. First step is adding the needed information to the pertinent YAML file. At this point is a matter of design taste. Do we prefer to add a new device or do we want to add it as a simple parameter for the experiment?

If we feel the shutter is going to become an important piece in the experiment or that we can have several shutters and want to address them in a convenient way, we should consider adding it as a device. On the other hand, if the shutter is just a step of the experiment, that we set once and forget about, we can directly include it as a step in the measurement process. In this guide we will opt for the latter.

Therefore, we add the next few lines to our YAML::

  shutter:
    port: PFI1
    delay: 100ms

It is an extra entry, at the same level than the axis or the detectors. The port is where the device is plugged; the delay is how long it takes before the shutter opens and a new line scan starts.

Now we have the parameters we need, there is no more need of information. However, this information has to be interpreted and used by the experiment class. Let's pretend at this stage that there is no shutter routine added yet. If we check how the experiment works, we can quickly see that the `do_line_scan` method is the place to add our code. We want the shutter to be closed for a certain amount of time before doing a wavelength scan, and we want to close it right after.

The delay is easy to control with a `time.sleep()` command, but opening and closing the shutter has to be addressed differently. As you see from the YAML file, we just define the shutter with a port; this is assuming the shutter is connected to the NI card. Even though this gives less flexibility, if we are aware, a quick and dirty solution may be all what we are looking for. This means, we can directly control the shutter with the NI card, and we shouldn't iterate through all the DAQs to see which one is supposed to generate the TTL signal we need.

However, we see that the model used for controlling the NI card (found at `model.daq.ni`) does not possess a method for digital outputs.

.. note:: This entire example is based on a real world case. This means that everything that is described here was already implemented into the code.

To summarize, what we need is the following:
    - Add to the YAML file the parameters we need
    - Add to the NI card the control over digital outputs.
    - Add to the experiment routine the delay and the open/close shutter
    - Add the possibility to change the delay into the GUI

Expanding the NI toolbox
~~~~~~~~~~~~~~~~~~~~~~~~
Starting with the NI class has the advantage that it is very easy to check if what we are doing makes sense. It also quickly provides insight into what can we be missing. Imagine you need to determine another parameter besides the port, etc. The outcome of this section should be that you can change the status of a given digital port from low to high or the opposite.

Relaying on pyDAQmx means that we can directly look into the `documentation provided by NI <http://zone.ni.com/reference/en-XX/help/370471AA-01/>`_. It is a vast amount of information that you should learn how to surf in order to survive. If you have a bit of experience with NI cards, you should probably know that the workflow starts by creating a task. It looks like this::

    import PyDAQmx as nidaq
    t = nidaq.Task()

Then we have to `create a channel <http://zone.ni.com/reference/en-XX/help/370471AA-01/daqmxcfunc/daqmxcreatedochan/>`_. The documentation gives us this information::

    int32 DAQmxCreateDOChan (TaskHandle taskHandle, const char lines[], const char nameToAssignToLines[], int32 lineGrouping);

This translates into pyDAQmx syntax like this::

    t.CreateDOChan(channel, None, nidaq.DAQmx_Val_ChanPerLine)

We have removed the reference to the `taskHandle` because it is implicitly passed as the first argument of the task `t`. Second, we remove teh `DAQmx` from the name of the function. To form the `channel` string, we do the following::

    channel = "Dev%s/%s" % (self.daq_num, port)

In this case the `self.daq_num` is storing the number of the DAQ; this is done at the instantiation of the NI class by the experiment class. The last variable is just how we are going to group the information. Since we are dealing with one channel at the time, we just done care.

Now we have a task that has a digital output channel available. Now we have to write to that output. Surfing through the documentation, within the `Write Functions <http://zone.ni.com/reference/en-XX/help/370471AA-01/daqmxcfunc/daqmxwritedigitalscalaru32/>`_ we find what we need::

    int32 DAQmxWriteDigitalScalarU32 (TaskHandle taskHandle, bool32 autoStart, float64 timeout, uInt32 value, bool32 *reserved);

Again, this translates into pyDAQmx code::

    t.WriteDigitalScalarU32(nidaq.bool32(True), 0, status, None)

We set it to autostart in order to skip the step of triggering the task. The rest you can understand it by reading the documentation. The only thing we need to define is what status is. If we want to use `True` as high and `False` as low, we can do it::

    status = 0
    if status:
        status = -1  # With this value, the digital output is set to High

The final function inside the class therefore looks like this::

    def digital_output(self, port, status):
        """ Sets the port of the digital_output to status (either True or False)
        """
        t = nidaq.Task()
        channel = "Dev%s/%s" % (self.daq_num, port)
        t.CreateDOChan(channel, None, nidaq.DAQmx_Val_ChanPerLine)

        if status:
            status = -1  # With this value, the digital output is set to High
        else:
            status = 0
        print('Status: {}'.format(status))
        t.WriteDigitalScalarU32(nidaq.bool32(True), 0, status, None)

And now we have to test it by adding these lines to the end of the file (adapt to your own needs)::

    if __name__ == '__main__':
        a = ni(2)
        status = True
        while True:
            status = not status
            a.digital_output('PFI1', status)
            input()

Plug a multimeter to the port you want to check and run the code. Do you see it changing from high to low? Great job then!

Updating the experiment logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Now that we know the NI can control the shutter via a TTL signal, we have to update the logic of our experiment. In the case of the Pharos, it means updating `model.experiment.measurement`. The details of this class are found in its own documentation page :doc:`experiment_class`

The way the 2D scan is done, is within a loop in the method `do_scan`::

    for value in np.linspace(start, stop, num_points_dev, endpoint=True):
        [...]
        self.do_line_scan()

We can either open and close the shutter in this loop, or we can do it directly inside the `do_line_scan`. The second approach gives us the advantage that the behavior is going to be the same every time we trigger a line scan, not necessarily from within the `do_scan` method. Therefore that is the file we are going to edit.

The first thing we have to do is to get the shutter parameters that were loaded into the class through the YAML file. We also grab the NI DAQ device from within the devices dictionary::

    shutter = self.scan['shutter']
    ni_daq = self.devices['NI-DAQ']

Now we only have to close the shutter, wait a `delay` time, open the shutter and do a wavelength scan::

    ni_daq.driver.digital_output(shutter['port'], False)
    delay = shutter['delay']
    time.sleep(delay)
    ni_daq.driver.digital_output(shutter['port'], True)
    laser.driver.execute_sweep()
    ni_daq.driver.digital_output(shutter['port'], False)

The code is simplified for example purposes. But you see that the logic is quite clear. It really reflects what was defined as a thought experiment. Of course, there are few things we should also address. For example, the delay that we defained in the YAML has units, while the sleep function takes seconds. Fortunately, the program was built with `Quantities` all over the place. If you want to have fun, try the following code::

    >>> from lantz import Q_
    >>> dist = Q_('1nm')
    >>> print(dist)
    >>> dist_pm = dist.to('pm')
    >>> print(dist_pm)
    >>> dist_in = dist.m_as('in')
    >>> print(dist_in)

The last couple of lines tells you that you can get the magnitude of a certain quantity in whichever units you want. So we do the same::

    delay = Q_(shutter['delay'])
    delay = delay.m_as('s')
    time.sleep(delay)

Now it doesn't really matter if you specify the delay in seconds, milliseconds or hours. The important thing is that it should always be a time unit.

Finally, you should notice that the shutter and the digital output may not be synchronized. The shutter opens with a LOW=>HIGH edge, and closes with a HIGH=>LOW. If when you switch on, the shutter is closed and the port is High, you will be out of sync; if you set to port to high, there will be no edge and therefore nothing will happen. The way around it is to include a function that you trigger at the beginning of your program, the synchronizes the digital port and the shutter::

    def sync_shutter(self):
        shutter = self.scan['shutter']
        ni_daq = self.devices['NI-DAQ']
        ni_daq.driver.digital_output(shutter['port'], False)
        time.sleep(0.2)
        ni_daq.driver.digital_output(shutter['port'], True)
        time.sleep(0.2)
        ni_daq.driver.digital_output(shutter['port'], False)

It is not an elegant solution, but it works. You do an antire cycle, finishing with the shutter closed. This guarantees that the digout and the shutter will be on the same page, when you set the digital output to High, the shutter opens, etc.

And now, you are done with everything. You just need to update your GUI to add support for this new feature.

.. todo:: Write the documentation on how to add it to the GUI.