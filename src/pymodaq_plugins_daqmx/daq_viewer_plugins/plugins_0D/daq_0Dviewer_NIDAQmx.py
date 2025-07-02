from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_Viewer import DAQ_NIDAQmx_Viewer


class DAQ_0DViewer_NIDAQmx(DAQ_NIDAQmx_Viewer):
    """
    Plugin for a 0D data visualization & acquisition with various NI modules plugged in a NI cDAQ.
    """
    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state, control_type='0D')
