"""
    start_gui
    =========
    Starting point for the GUI of the program. It loads the configuration files and starts the experiment class.
    Then it builds the main Window GUI.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
import sys
import os
from PyQt4.Qt import QApplication

from pharos.view.main_window import MainWindow
from pharos.model.lib.general_functions import from_yaml_to_dict
from pharos.model.experiment.measurement import Measurement

os.environ['PATH'] = os.environ['PATH'] + ';' + 'C:\\Program Files (x86)\\Thorlabs\\Kinesis'

config_experiment = "config/measurement.yml"
experiment_dict = from_yaml_to_dict(config_experiment)
experiment = Measurement(experiment_dict)
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.connect_monitor_devices_to_daq()
experiment.sync_shutter()
# Starting the GUI
ap = QApplication(sys.argv)
m = MainWindow(experiment)
m.show()
ap.exit(ap.exec_())