import numpy as np
from pymodaq_data import DataToExport
from pymodaq.utils.data import DataFromPlugins
from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_Viewer import DAQ_NIDAQmx_Viewer


class DAQ_1DViewer_NIDAQmx(DAQ_NIDAQmx_Viewer):
    """
    Plugin for bufferized 1D data visualization & acquisition with NI modules (plugged in NI cDAQ or NI-USB).
    """
    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state, control_type='1D')
