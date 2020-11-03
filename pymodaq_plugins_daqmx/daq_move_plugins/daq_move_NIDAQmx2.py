from ..hardware.national_instruments.daq_NIDAQmx import DAQ_NIDAQmx_Actuator


class DAQ_Move_NIDAQmx2(DAQ_NIDAQmx_Actuator):
    """
        ==================== ========================
        **Attributes**         **Type**
        *data_grabed_signal*   instance of pyqtSignal
        *params*               dictionnary list
        *task*
        ==================== ========================

        See Also
        --------
        refresh_hardware
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

