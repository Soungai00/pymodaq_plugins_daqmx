import numpy as np
from pymodaq_data import DataToExport
from pymodaq.utils.data import DataFromPlugins
from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_Viewer import DAQ_NIDAQmx_Viewer


class DAQ_1DViewer_NIDAQmx(DAQ_NIDAQmx_Viewer):
    """
    Plugin for a 0D data visualization & acquisition with various NI modules plugged in a NI cDAQ.
    """
    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state, control_type='1D')

    def emit_data(self, task_handle, every_n_samples_event_type, number_of_samples, callback_data):
        channels_names = [ch.name for ch in self.channels]
        data_from_task = self.controller.task.read(self.settings['nsamplestoread'], timeout=20.0)
        if not len(self.controller.task.channels.channel_names) != 1:
            data_dfp = [np.array(data_from_task)]
        else:
            data_dfp = list(map(np.array, data_from_task))
        self.dte_signal.emit(DataToExport(name='NIDAQmx',
                                          data=[DataFromPlugins(name='NI Analog Input',
                                                                data=data_dfp,
                                                                dim=f'Data{self.control_type}',
                                                                labels=channels_names,
                                                                ),
                                                ]))
        return 0  # mandatory for the NIDAQmx callback