from ..hardware.national_instruments.NIDAQmx_Move import DAQ_NIDAQmx_Actuator
from pymodaq.control_modules.move_utility_classes import main


class DAQ_Move_NIDAQmx(DAQ_NIDAQmx_Actuator):
    """
        Plugin for basic current or voltage control with NI modules (plugged in NI cDAQ or NI-USB). (in process)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    main(__file__, init=False)
