Using the 1D viewer Nidaqmx
===========================

This plugin is meant to be used to make measurement and acquire analog data with a NI card. According to the material used, a lot of physical quantity can be detected. Until August 2025, you can measure temperatures, currents or voltages.

.. note::
    Stay aware of the maximum quantity measurable which depends on what can supports your device.

It was tested only with a cDAQ-9174 with modules NI-9205 and NI-9211 devices.

Configuration
-------------

You need to provide those parameters (or at least be aware of the default settings), as shown in the screenshot below.

* **Devices**: The device you want to use among each detected device. It can be the whole cDAQ, such as ``/cDAQ[X]``, or a specific module, such as ``/cDAQ[X]Mod[Y]``.

* **Signal type**: the type of measurement you want to make (mostly ANALOG_INPUT since digital measurements are not supported yet and output signals do not concern viewers but daq_move).

* **NSamples To Read**: the number of samples displayed by the viewer

* **Plugin config**: A push button loading a specific configuration set by the user.
    It aims to prevent from multiple channel entry each time the plugin is loaded. It is very useful in the case of setups including many modules / channels, for exemple with one experimental bench being used for multiples measurement campaigns.
    To make your configuration, refer to the example shown in the file ``C:\ProgramData\.pymodaq.\config_daqmx.toml`` and fill the file ``C:\Users\<user>\.pymodaq.\config_daqmx.toml`` with your own material (syntax needs to be respected to prevent from errors).

* **Clock Settings - Nsamples**: The number of samples requested to the material for each channel

* **Clock Settings - Frequency**: the acquisition rate, which is common for each acquisition channel.

* **AI Channels**: the channel(s) you will use for your analog measurements, something like ``cDAQ[X]Mod[Y]/ai[Z]``. You can generate it directly or load it automatically using the plugin config. Pay attention not creating the same channel twice!

  .. image:: /images/parameters.png
    :width: 800

This plugin is not intended to be used with a "Slave" configuration, but you can definitely use the same NI card device as hardware for other plugins at the same time.

Be careful to use as photon source the default input terminal corresponding to the counting channel, check the documentation of your NI device about this.


Use
---

It works as a usual 1D viewer plugin.

If you encounter some problems, you might get some warnings or errors in the log, check it to get some hints to solve it.
You can run ``Get-Content .pymodaq\log\pymodaq.log -Tail 10 -Wait`` in the PowerShell to display the log in real time.
