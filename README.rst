pymodaq_plugins_daqmx (National Instrument DAQmx)
#################################################

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_daqmx.svg
   :target: https://pypi.org/project/pymodaq_plugins_daqmx/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_daqmx/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_daqmx

Plugin devoted to the National Instrument signal acquisition and generation using the NiDAQmx library. Includes an
actuator plugin for signal generation, a 1D viewer plugin for data acquisition as a function of time and a 0D viewer
plugin for quick time averaging acquisition

Authors
=======

* Sébastien J. Weber

Contributors
============

* Amelie Jarnac
* Aurore Finco
* Sébastien Guerrero  (sebastien.guerrero@insa-lyon.fr)

Instruments
===========
Below is the list of instruments included in this plugin

Actuators
+++++++++

* **DAQmx_MultipleScannerControl**: Control of piezo scanners with an analog output.

Viewer0D
++++++++

* **DAQmx_PLcounter**: Single photon counting
* **NIDAQmx**: General measurement with National Instrument materials

NIDAQmx Viewer
++++++++++++++

This viewer aims at being very general and allows measurement with as much different NI modules as possible.
At this point (06/2025), it supports Analog measurement of currents, voltages and temperatures from thermocouples.

Tests have been running with the following devices:
    * Chassis NI cDAQ-9174 & NI USB-9162
    * NI modules 9211 & 9205

Acquisition channels can ge generated directly running the viewer, but it is also possible to load channels from the configuration file config_daqmx.toml clicking on "load configuration" in the parameter tree

To use such configuration, copy paste the content from C:/ProgramData/.pymodaq/config_daqmx.toml to <user_path>/.pymodaq/config_daqmx.toml and fill it with the configuration of your own experimental setup.