# please add comments to clarify!

import PyDAQmx as nidaq

ni_buffer = 50000  # When acquiring in continuous mode, how big is the buffer.
ni_measure_mode = nidaq.DAQmx_Val_Diff
ni_trigger_edge = nidaq.DAQmx_Val_Rising
ni_read_timeout = 0.1
monitor_read_scan = 10  # How many times do we update the signal during 1 wavelength sweep