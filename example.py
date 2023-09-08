# NIDAQTest.py

from NIDAQClient import NIDAQVoltage
from NIDAQClient import NIDAQThermo

# Create an instance of the client for thermocouple reading.
# This thermocouple module is installed in position 2 in the NI DAQ cage:
daq = NIDAQThermo(position=2, thermocouple_type='J')
daq.start()

# Here, use the `read_samples` method whenever you need to read from the channels.
data = daq.read_samples()

# Print the data here in the console
print("Received Thermocouple Data:")
print(data)

daq.stop()
daq.close()



# Now, read a voltage sensor installed in the NI cage in position 4:
daq = NIDAQVoltage(position=4)
daq.start()

# Here, use the `read_samples` method whenever you need to read from the channels.
data = daq.read_samples()

# Print the data here in the console
print("Received Voltage Data:")
print(data)

daq.stop()
daq.close()