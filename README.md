# Pharos Controller v0.2 #

This controller is responsible for the Pharos setup at Utrecht University. 

The Pharos setup relies on a Santec laser able to scan wavelengths at variable ranges and speeds; the design of the software was therefore planned around the laser. Each scan will have as a principal axis the wavelength, while a secondary axis can be time or any property of another device.

## Goals ##

1. [x] Monitor N-Signals while the laser is scanning
2. [x] Monitor the signals also when doing a 2-way scan
3. [x] Save the data to the desired folder
4. [x] Build a non-GUI alternative allowing the repetition of experiments
5. [x] Perform N-dimensional scans while aquiring M-different signals
6. [x] Monitor the signals while being recorded within a GUI.
7. [x] Split the program into the non-GUI and the GUI specific for Pharos.