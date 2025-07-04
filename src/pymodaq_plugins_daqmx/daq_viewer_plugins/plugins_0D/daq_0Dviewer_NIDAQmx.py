import numpy as np
from pymodaq_data import DataToExport
from pymodaq.utils.data import DataFromPlugins
from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_Viewer import DAQ_NIDAQmx_Viewer


class DAQ_0DViewer_NIDAQmx(DAQ_NIDAQmx_Viewer):
    """
    Plugin for a 0D data visualization & acquisition with various NI modules plugged in a NI cDAQ.
    Warning: This 0D viewer is a quick solution for sending 0D data and keeping track of history,
    Since it recombines arrays from buffer to send it in 0D, it only supports low acquisition rate
    """
    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state, control_type='0D')

    def emit_data(self, task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        channels_names = [ch.name for ch in self.channels]
        data_from_task = self.controller.task.read(self.settings['nsamplestoread'], timeout=20.0)
        for i in range(self.settings['nsamplestoread']):
            if len(self.controller.task.channels.channel_names) == 1:
                data_dfp = np.array([data_from_task[i]])
            else:
                data_dfp = np.array([data[i] for data in data_from_task])
            self.dte_signal.emit(DataToExport(name='NIDAQmx',
                                              data=[DataFromPlugins(name='NI Analog Input',
                                                                    data=[np.array([data_dfp[i]]) for i in
                                                                          range(len(data_dfp))],
                                                                    dim=f'Data{self.control_type}',
                                                                    labels=channels_names
                                                                    ),
                                                    ]))
        return 0  # mandatory for the NIDAQmx callback
