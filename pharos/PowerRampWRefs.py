"""
    start_measurement
    =================
    Starting point for a measurement without GUI. It is mainly an example of how things should be built from the ground
    up in order to later have a GUI.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""

import sys

from time import sleep
from lantz import Q_

from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.measurement import Measurement

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

config_experiment = "config/PowerRampWRefs_measurement.yml"

experiment_dict = from_yaml_to_dict(config_experiment)
print(experiment_dict['scan']['axis'])
experiment = Measurement(experiment_dict)

# start_logger('test.log')
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.connect_monitor_devices_to_daq()    
experiment.sync_shutter()
experiment.scan['laser']['params'].update({
    'start_wavelength': Q_(experiment.scan['laser']['params']['start_wavelength']),
    'stop_wavelength': Q_(experiment.scan['laser']['params']['stop_wavelength']),
    'wavelength_speed': Q_(experiment.scan['laser']['params']['wavelength_speed']),
    'interval_trigger': Q_(experiment.scan['laser']['params']['interval_trigger']),
    'wavelength_sweeps': Q_(experiment.scan['laser']['params']['wavelength_sweeps']),
})

experiment.setup_scan()
print('------ DO SCANS -------')
experiment.do_scans_with_ref(1) # nr of runs you want to do per power between brackets
#experiment.do_scan() 

print('--> ', Q_(experiment_dict['scan']['axis']['device']['range'][0]))

#start figure
fig = plt.figure(figsize = (16,12))#figsize = (14,5)
x_formatter = mpl.ticker.ScalarFormatter(useOffset=False)

#calculate the x-axis (scanning properties)
laser_params = experiment.scan['laser']['params']
start_wavelength = laser_params['start_wavelength']
stop_wavelength  = laser_params['stop_wavelength']
interval_trigger = laser_params['interval_trigger']
num_points = (laser_params['stop_wavelength'] - laser_params['start_wavelength']) / laser_params['interval_trigger']
num_points = (int(round(num_points.m_as('')))+1) * laser_params['wavelength_sweeps']
xval = np.linspace(start_wavelength,stop_wavelength, num_points)




### READ ALL THE DATA ###
print('------ READ DATA -------')
#data_scan = experiment.read_scans(2)
#print('has been read')
#for d in data_scan:
#    print('check what is in data_scan')
#    #print(d, data_scan[d])
#    print(d, len(data_scan[d]))
#    print(num_points)
data_scan = experiment.scan_data
for i in range(len(data_scan)):
    data = data_scan[i]
    for d in data:
        print('Length of {}: {}'.format(d,len(data[d])))
        
sys.exit()
    
#NOTES
#questions, this way you will put all the data in de daq memory, and aquire after the scans have finised. won't you run out of enough memory??
#for the reference scan an extra row at read_scans is needed -->added extra option to read_scans

i = 1
for d in data_scan:
    data_dummy = []
    data_dummy.append(xval)
    k = 230 + i
    ax = fig.add_subplot(k)
    #print('len data = ', len(data_scan[d]))
    #print(d)
    #print(data_scan[d][0])
    ax.xaxis.set_major_formatter(x_formatter)
    
    #seperate data into wavelength, forward/backward scans, angles
    for j in range(int(len(data_scan[d])/num_points)):
        data_dummy.append(data_scan[d][int(j*num_points):(j+1)*int(num_points)])
        ax.plot(data_dummy[0],data_dummy[j+1])
        #every even index (>0) of data_dummy = a reference scan)
  
    ax.set_title(d)
    ax.set_ylabel('signal (V)')
    ax.set_xlabel('wavelength (nm)')
    np.savetxt(d+'_',data_dummy,delimiter=',')
    i+=1

    
### CHECK IF THERE IS REMAINING DATA IN THE DAQ ###
data_scan = experiment.read_scans(-1)
for d in data_scan:
    print('check if daq is empty')
    print(d)
    print(d, data_scan[d])
    
    
experiment.stop_scan()


plt.show()

# stop_logger()

#shutter: -1 is open