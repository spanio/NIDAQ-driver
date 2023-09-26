import numpy as np
import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx import constants
from nidaqmx.constants import AcquisitionType, TemperatureUnits, ThermocoupleType, TerminalConfiguration

class NIDAQVoltage:
    def __init__(self, position, sampling_freq_in=500, buffer_in_size=100000):

        # Check for valid position in the NI DAQ cage
        if position not in [1, 2, 3, 4]:
            raise ValueError("Invalid position value. Must be 1, 2, 3, or 4.")
        
        self.position = position
        self.chans_in = 32
        self.channel_names = [f"Voltage Channel {i+1}" for i in range(self.chans_in)]
        self.sampling_freq_in = sampling_freq_in
        self.buffer_in_size = buffer_in_size
        self.buffer_in_size_cfg = round(self.buffer_in_size * 1)
        self.bufsize_callback = self.buffer_in_size
        self.task_in = nidaqmx.Task()
        self.configure_task()
        self.stream_in = AnalogMultiChannelReader(self.task_in.in_stream)
        self.buffer_in = np.zeros((self.chans_in, self.buffer_in_size))
        
    def configure_task(self):
        channel_string = f"cDAQ1Mod{self.position}/ai0:31"
        self.task_in.ai_channels.add_ai_voltage_chan(channel_string, terminal_config=TerminalConfiguration.NRSE)
        self.task_in.timing.cfg_samp_clk_timing(rate=self.sampling_freq_in, sample_mode=constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.buffer_in_size_cfg)
        self.task_in.in_stream.input_buf_size = self.bufsize_callback
        
    def read_samples(self):

        buffer_in = np.zeros((self.chans_in, 500))
        self.stream_in.read_many_sample(buffer_in, 500, timeout=constants.WAIT_INFINITELY)
        
        # Calculate the RMS for each channel.
        rms_values = np.sqrt(np.mean(buffer_in**2, axis=1))
        rounded_rms_values = np.round(rms_values, 5)
        return rounded_rms_values
    

    
    def get_channel_names(self):
        return self.channel_names
    
    def set_channel_name(self, position, name):
        """
        Set the name of a specific channel based on its position.

        Args:
            position (int): Position of the channel (0-based index).
            name (str): New name for the channel.
        """
        if position < 0 or position >= self.chans_in:
            raise ValueError(f"Invalid position value. Must be between 0 and {self.chans_in-1}.")
        self.channel_names[position] = name

    
    def start(self):
        self.task_in.start()
        
    def stop(self):
        self.task_in.stop()
        
    def close(self):
        self.task_in.close()


class NIDAQThermo:
    def __init__(self, position, thermocouple_type='J', sampling_freq_in=500, buffer_in_size=100000):

        # Check for valid position in the NI DAQ cage
        if position not in [1, 2, 3, 4]:
            raise ValueError("Invalid position value. Must be 1, 2, 3, or 4.")
        
         # Check for valid thermocouple type
        allowed_thermocouple_types = ['B', 'E', 'J', 'K', 'N', 'R', 'S', 'T']
        if thermocouple_type not in allowed_thermocouple_types:
            raise ValueError(f"Invalid thermocouple type. Must be one of {allowed_thermocouple_types}.")
        
        self.thermocouple_type = getattr(ThermocoupleType, thermocouple_type)
        self.position = position

        self.chans_in = 8
        self.channel_names = [f"Thermo Channel {i+1}" for i in range(self.chans_in)]
        self.sampling_freq_in = sampling_freq_in
        self.buffer_in_size = buffer_in_size
        self.buffer_in_size_cfg = round(self.buffer_in_size * 1)
        self.bufsize_callback = self.buffer_in_size
        self.task_in = nidaqmx.Task()
        self.configure_task()
        self.stream_in = AnalogMultiChannelReader(self.task_in.in_stream)
        self.buffer_in = np.zeros((self.chans_in, self.buffer_in_size))
        
    def configure_task(self):
        channel_string = f"cDAQ1Mod{self.position}/ai0:7"
        self.task_in.ai_channels.add_ai_thrmcpl_chan(channel_string, units=TemperatureUnits.DEG_C, thermocouple_type=self.thermocouple_type)
        self.task_in.timing.cfg_samp_clk_timing(rate=self.sampling_freq_in, sample_mode=constants.AcquisitionType.CONTINUOUS, samps_per_chan=self.buffer_in_size_cfg)
        self.task_in.in_stream.input_buf_size = self.bufsize_callback
        
    def read_samples(self):

        buffer_in = np.zeros((self.chans_in, 500))
        self.stream_in.read_many_sample(buffer_in, 500, timeout=constants.WAIT_INFINITELY)
   
        
        # average and round the values for each channel
        rms_values = np.mean(buffer_in, axis=1)  #this is not actually RMS'd. just trust me bro
        rounded_values = np.round(rms_values, 2)
        return rounded_values
    

    
    def get_channel_names(self):
        return self.channel_names
    
    def set_channel_name(self, position, name):
        """
        Set the name of a specific channel based on its position.

        Args:
            position (int): Position of the channel (0-based index).
            name (str): New name for the channel.
        """
        if position < 0 or position >= self.chans_in:
            raise ValueError(f"Invalid position value. Must be between 0 and {self.chans_in-1}.")
        self.channel_names[position] = name

    
    def start(self):
        self.task_in.start()
        
    def stop(self):
        self.task_in.stop()
        
    def close(self):
        self.task_in.close()