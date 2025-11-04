import nidaqmx
import numpy as np
import traceback
from .daqmxni import NIDAQmx, niDevice
from pymodaq_plugins_daqmx.hardware.national_instruments.NIDAQmx_base import DAQ_NIDAQmx_base, TerminalConfiguration, \
    UsageTypeAI, ChannelType
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters as viewer_params
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.utils.logger import set_logger, get_module_name
logger = set_logger(get_module_name(__file__))


class DAQ_NIDAQmx_Viewer(DAQ_Viewer_base, DAQ_NIDAQmx_base):
    """
        ==================== ========================
        **Attributes**         **Type**
        *data_grabed_signal*   instance of Signal
        *params*               dictionary list
        *task*
        ==================== ========================

        See Also
        --------
        refresh_hardware
    """
    config_channels: list
    controller: NIDAQmx
    config_devices: list
    config_modules: list
    live: bool
    Naverage: int
    param_devices = NIDAQmx.get_NIDAQ_devices().device_names
    params = viewer_params + [
        {'title': 'Devices :', 'name': 'devices', 'type': 'list', 'limits': param_devices,
         'value': param_devices[0]
         },
        ] + DAQ_NIDAQmx_base.params

    def __init__(self, parent=None, params_state=None, control_type="0D"):
        DAQ_Viewer_base.__init__(self, parent, params_state)  # defines settings attribute and various other methods
        DAQ_NIDAQmx_base.__init__(self)

        self.Naverage = None
        self.live = False
        self.control_type = control_type  # could be "0D", "1D"
        if self.control_type == "0D":
            self.settings.child('NIDAQ_type').setLimits([ChannelType.ANALOG_INPUT.name,
                                                         ChannelType.COUNTER_INPUT.name,
                                                         ChannelType.DIGITAL_INPUT.name])
        elif self.control_type == "1D":
            self.settings.child('NIDAQ_type').setLimits([ChannelType.ANALOG_INPUT.name])

        self.settings.child('ao_settings').hide()
        self.settings.child('ao_channels').hide()

    def ini_attributes(self):
        super().ini_attributes()
        self.config_channels = []
        self.config_devices = []
        self.config_modules = []
        self.live = False
        self.Naverage = 1

    def ini_detector(self, controller=None):
        """
            Initialisation procedure of the detector.

            See Also
            --------
            daq_utils.ThreadCommand
        """
        try:
            if self.is_master:
                self.controller = NIDAQmx()
            else:
                self.controller = controller
            self.controller.device = nidaqmx.system.Device(self.settings["devices"])

            # actions to perform in order to set properly the settings tree options
            self.commit_settings(self.settings.child('NIDAQ_type'))

            info = "Plugin Initialized"
            initialized = True
            logger.info("Detector {} initialized".format(self.control_type))
            return info, initialized

        except Exception as e:
            logger.info(traceback.format_exc())
            self.emit_status(ThreadCommand('Update_Status', [str(e), 'log']))
            info = str(e)
            initialized = False
            return info, initialized

    def commit_settings(self, param):
        """
            Activate the parameters changes in the hardware.

            =============== ================================ ===========================
            **Parameters**   **Type**                        **Description**
            *param*         instance of pyqtgraph.parameter   the parameter to activate
            =============== ================================ ===========================

            See Also
            --------
            update_NIDAQ_channels, update_task, refresh_hardware
        """
        DAQ_NIDAQmx_base.commit_settings(self, param)

        if param.parent() is not None:
            if param.parent().name() == 'ai_channels':
                device = param.opts['title'].split('/')[0]
                self.settings.child('clock_settings', 'frequency').setOpts(max=self.controller.getAIMaxSingleRate(device))
                volt_ranges = self.controller.getAIVoltageRange(device)
                if volt_ranges:
                    param.child('voltage_settings', 'volt_min').setValue(volt_ranges[0])
                    param.child('voltage_settings', 'volt_max').setValue(volt_ranges[1])
                curr_ranges = self.controller.getAICurrentRange(device)
                if curr_ranges:
                    param.child('current_settings', 'curr_min').setValue(curr_ranges[0])
                    param.child('current_settings', 'curr_max').setValue(curr_ranges[1])
            elif param.name() == 'devices':
                self.controller.device = self.settings.child('devices')
            elif param.name() == 'load_config':
                self.controller.configuration_sequence(self, self.controller.device)
                self.settings.child('load_config').hide()
                config_ai_channels = [ch for ch in self.config_channels if ch.source == ChannelType.ANALOG_INPUT]
                for ch in config_ai_channels:  # Browse configuration analog channels
                    self.settings.child('ai_channels').addNew(ch.name)
                    ch_par = [a for a in self.settings.child('ai_channels').childs if a.opts['title'] == ch.name][0]
                    ch_par.child("voltage_settings").show(ch.analog_type == UsageTypeAI.VOLTAGE)
                    ch_par.child("current_settings").show(ch.analog_type == UsageTypeAI.CURRENT)
                    ch_par.child("thermoc_settings").show(ch.analog_type == UsageTypeAI.TEMPERATURE_THERMOCOUPLE)
                    match ch.analog_type:
                        case UsageTypeAI.VOLTAGE:
                            self.settings.child("ai_channels", ch_par.opts['name'], "ai_type").setValue("VOLTAGE")
                            self.settings.child("ai_channels", ch_par.opts['name'], "voltage_settings",
                                                "volt_min").setValue(
                                ch.value_min)
                            self.settings.child("ai_channels", ch_par.opts['name'], "voltage_settings",
                                                "volt_max").setValue(
                                ch.value_max)
                            self.settings.child("ai_channels", ch_par.opts['name'], "termination").setValue(
                                ch.termination.name)
                        case UsageTypeAI.CURRENT:
                            self.settings.child("ai_channels", ch_par.opts['name'], "ai_type").setValue("CURRENT")
                            self.settings.child("ai_channels", ch_par.opts['name'], "current_settings",
                                                "curr_min").setValue(
                                ch.value_min)
                            self.settings.child("ai_channels", ch_par.opts['name'], "current_settings",
                                                "curr_max").setValue(
                                ch.value_max)
                            self.settings.child("ai_channels", ch_par.opts['name'], "termination").setValue(
                                ch.termination.name)
                        case UsageTypeAI.TEMPERATURE_THERMOCOUPLE:
                            self.settings.child("ai_channels", ch_par.opts['name'], "ai_type").setValue(
                                "TEMPERATURE_THERMOCOUPLE")
                            self.settings.child("ai_channels",
                                                ch_par.opts['name'],
                                                "thermoc_settings",
                                                "thermoc_type").setValue(ch.thermo_type.name)
                            self.settings.child("ai_channels",
                                                ch_par.opts['name'],
                                                "thermoc_settings",
                                                "T_min").setValue(ch.value_min)
                            self.settings.child("ai_channels",
                                                ch_par.opts['name'],
                                                "thermoc_settings",
                                                "T_max").setValue(ch.value_max)
                            self.settings.child("ai_channels", ch_par.opts['name'], "termination").setValue(
                                TerminalConfiguration.DEFAULT.name)
                self.channels = self.get_channels_from_settings()
                self.set_max_frequency()  # Set the acquisition frequency to the device maximum frequency
            self.channels = self.get_channels_from_settings()
            self.get_max_frequency()  # Set the frequency 'max' option to the device maximum frequency and display it

    def get_max_frequency(self):
        # Destined to be removed when set_max_frequency will work correctly
        try:
            max_freq = int(self.controller.getAIMaxSingleRate(self.controller.device.name))
            self.settings.child('clock_settings', 'max_freq').setValue(max_freq)
        except:
            pass

    def set_max_frequency(self):
        # Opts 'max' get the right value but doesn't update the viewer which keep as max the initial max value
        try:
            max_freq = int(self.controller.getAIMaxSingleRate(self.controller.device.name))
            self.settings.child('clock_settings', 'frequency').setOpts(max=max_freq)
            self.settings.child('clock_settings', 'frequency').emitStateChanged('max', max_freq)
            self.settings.child('clock_settings', 'frequency')._emitOptionsChanged(
                self.settings.child('clock_settings', 'frequency'), {'max': max_freq})
        except:
            pass

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        try:
            DAQ_NIDAQmx_base.stop(self)
            self.live = False
            logger.info("Acquisition stopped.")
        except Exception:
            pass
        self.emit_status(ThreadCommand('Update_Status', ['Acquisition stopped.']))
        return ''

    def close(self):
        self.live = False
        self.stop()
        self.controller.close()
