# NIDAQ-driver
 Python library for NI DAQ modules

To use, include NIDAQClient.py in your project.

# Example
```python
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
```

The output will look something like this:
```
Received Thermocouple Data:
[1376.34 1376.34 1376.34 1376.34 1376.34 1376.34 1376.34 1376.34]
Received Voltage Data:
[3.27506 3.27454 3.31136 3.29971 3.32641 3.30917 3.33307 3.3026  3.16697
 3.15747 3.18815 3.15947 3.19679 3.17848 3.19905 3.16965 3.25606 3.25605
 3.29187 3.28341 3.30896 3.29355 3.31831 3.29019 3.16315 3.15645 3.18703
 3.16075 3.19613 3.17977 3.19904 3.1716 ]
 ```

 # Usage

 The NI DAQ 'cards' must be addressed by their position in the cage. The cage positions are represented in the ASCII art below:

 ```
 -----------------------------------------------
|             |       |       |       |       |
|  National   |   P   |   P   |   P   |   P   |
| Instruments |   O   |   O   |   O   |   O   |
|             |   S   |   S   |   S   |   S   |
|   NI cDAQ   |   I   |   I   |   I   |   I   |
|             |   T   |   T   |   T   |   T   |
|             |   I   |   I   |   I   |   I   |
|             |   O   |   O   |   O   |   O   |
|  []  USB    |   N   |   N   |   N   |   N   |
|  []  Power  |       |       |       |       |
|             |   1   |   2   |   3   |   4   |
|             |       |       |       |       |
-----------------------------------------------
```

For example if a thermocouple card is inserted in position 3, you must initalize the reader as
```python
daq = NIDAQThermo(position=2, thermocouple_type='J')
```

You can read the samples from the card with the following:
```python
data = daq.read_samples()
```

This code will return a list of values from the card. Thermocouple cards will return eight values, relating to thermocouple channels 0 through 7. Voltage cards will return thirty-two values, relating to channels 0 through 31. You can pull these values into the rest of your code to save or transmit to other parts of your code.