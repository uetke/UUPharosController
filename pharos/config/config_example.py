# please add comments to clarify!

import PyDAQmx as nidaq

# Defaults for the NI card
ni_buffer = 5000  # When acquiring in continuous mode, how big is the buffer.
ni_measure_mode = nidaq.DAQmx_Val_Diff  #
ni_trigger_edge = nidaq.DAQmx_Val_Rising
ni_start_edge = nidaq.DAQmx_Val_Rising
ni_read_timeout = 10

# Defaults for GUI
monitor_read_scan = 30  # How often (in milliseconds) do we update the signal during 1 wavelength sweep

# Defaults for the laser (mainly for sleep or timer arguments)
laser_update = 500   #  How often (in milliseconds) the laser properties are updated.
laser_refresh = 0.1  #  How often (in seconds) to check if the laser has finished scanning