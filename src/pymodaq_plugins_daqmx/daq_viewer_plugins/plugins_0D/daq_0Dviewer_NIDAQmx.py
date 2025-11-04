import numpy as np
from pymodaq_data import DataToExport
from pymodaq.utils.data import DataFromPlugins
from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_Viewer import DAQ_NIDAQmx_Viewer
from pymodaq_plugins_daqmx.hardware.national_instruments.daqmxni import Edge, ChannelType, ClockSettings, \
    TriggerSettings
from pymodaq.utils.logger import set_logger, get_module_name
logger = set_logger(get_module_name(__file__))

class DAQ_0DViewer_NIDAQmx(DAQ_NIDAQmx_Viewer):
    """
    Plugin for bufferized 0D data visualization & acquisition with NI modules (plugged in NI cDAQ or NI-USB).
    """
    live_mode_available = False

    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state, control_type='0D')

    def grab_data(self, Naverage=1, **kwargs):
        """
            | grab the current values with NIDAQ profile procedure.
            |
            | Send the data_grabed_signal once done.

            =============== ======== ===============================================
            **Parameters**  **Type**  **Description**
            *Naverage*      int       Number of values to average
            =============== ======== ===============================================
        """
        if self.controller.task is None:
            # In synchronous mode, acquisition rate does not come from clock settings but from each grab
            self.clock_settings = ClockSettings(frequency=self.settings['clock_settings', 'frequency'],
                                                Nsamples=self.settings['clock_settings', 'Nsamples'],
                                                edge=Edge.RISING,
                                                repetition=False, )
            self.controller.update_task(self.get_channels_from_settings(), self.clock_settings)

        if self.settings['NIDAQ_type'] == ChannelType.COUNTER_INPUT.name:
            self.timer.start(self.settings['counter_settings', 'counting_time'])

        channels_names = [ch.name for ch in self.channels]
        data_from_task = self.controller.task.read(timeout=20.0)
        data_dfp = list(map(lambda f: np.array([f]), data_from_task))
        self.dte_signal.emit(DataToExport(name='NIDAQmx',
                                          data=[DataFromPlugins(name='Data from ' + self.controller.device.name,
                                                                data=data_dfp,
                                                                dim=f'Data{self.control_type}',
                                                                labels=channels_names,
                                                                ),
                                                ]))
