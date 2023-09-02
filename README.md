# Multi-Agent-Deep-Reinforcement-Learning-for-Traffic-Signal-Control
# AT-Conv-LSTM and deeprl_signal_control

This repository contains two projects that integrate reinforcement learning (RL) techniques, specifically AT-Conv-LSTM, with the SUMO (Simulation of Urban MObility) traffic simulator. These projects aim to enhance traffic signal control in SUMO by leveraging deep reinforcement learning algorithms.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing SUMO](#installing-sumo)
- [Projects Overview](#projects-overview)
  - [AT-Conv-LSTM](#at-conv-lstm)
  - [deeprl_signal_control](#deeprl_signal_control)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Both projects are designed to improve traffic signal control through RL techniques. Before diving into the details of each project, you'll need to set up SUMO, the traffic simulation environment.

## Getting Started

### Prerequisites

To run these projects, you'll need:

- Python (version 3.x)
- TensorFlow
- SUMO (Simulation of Urban MObility)

### SUMO

#### About
-----

sumo, the SUpport MOdule manager, is a set of tools to support software
development for the `EPICS <https://epics.anl.gov>`_ framework. It manages
build dependencies and consistent builds of the 
`EPICS <https://epics.anl.gov>`_ base and `EPICS <https://epics.anl.gov>`_
support modules.

#### Author
------

Goetz Pfeiffer <Goetz.Pfeiffer@helmholtz-berlin.de>

#### Documentation
-------------

Documentation is available online here:

`sumo documentation <https://epics-sumo.sourceforge.io>`_.

Documentation is also included in the software distribution in HTML format.

#### Installation
------------

You can install sumo with `pip <https://pip.pypa.io/en/stable>`_
(python package manager), as 
`debian <https://www.debian.org/distrib/packages>`_  or 
`rpm <http://rpm.org>`_  package or from 
`source <https://docs.python.org/3/install>`_.

All is described here:

`sumo install <https://epics-sumo.sourceforge.io/sumo-install.html>`_.

License
-------

Sumo is licensed under GNU GPL v.3. Here is the license text:

`sumo license <https://epics-sumo.sourceforge.io/license.html>`_.

[SUMO Download Page](https://sumo.dlr.de/docs/Downloads.php)

Please follow the installation instructions provided on the SUMO website to ensure you have SUMO set up correctly.

## Projects Overview

### AT-Conv-LSTM

[AT-Conv-LSTM Project Repository](https://github.com/PeterMwendia/Multi-Agent-Deep-Reinforcement-Learning-for-Traffic-Signal-Control/tree/main/AT-Conv-LSTM)

- **Description**: AT-Conv-LSTM (Attention-based Convolutional LSTM) is a deep learning model designed for traffic signal control.
- **Project Structure**: The AT-Conv-LSTM project is organized into several folders, including:
  - `data`: Contains datasets or data processing scripts.
  - `models`: Contains the AT-Conv-LSTM model implementation.
  - `experiments`: Includes experiments and configuration files.
  - `results`: Stores the results of training and evaluation.
- **How It Works**: AT-Conv-LSTM combines convolutional layers with LSTM and attention mechanisms to optimize traffic signal control.

### deeprl_signal_control

[deeprl_signal_control Project Repository](https://github.com/PeterMwendia/Multi-Agent-Deep-Reinforcement-Learning-for-Traffic-Signal-Control/tree/main/deeprl_signal_control)

- **Description**: deeprl_signal_control integrates RL agents with SUMO for intelligent traffic signal control.
- **Project Structure**: The deeprl_signal_control project contains:
  - `agents`: Implementation of RL agents.
  - `envs`: Custom traffic environment configurations.
  - `utils`: Utility functions for training, testing, and evaluation.
- **How It Works**: This project provides a framework for training and evaluating RL agents in SUMO environments. It includes RL algorithms, traffic environment definitions, and evaluation tools.

## Usage

Detailed usage instructions for each project can be found in their respective repositories:

- [AT-Conv-LSTM README](https://github.com/PeterMwendia/Multi-Agent-Deep-Reinforcement-Learning-for-Traffic-Signal-Control/blob/main/AT-Conv-LSTM/README.md)
- [deeprl_signal_control README](https://github.com/PeterMwendia/Multi-Agent-Deep-Reinforcement-Learning-for-Traffic-Signal-Control/blob/main/deeprl_signal_control/README.md)

## Contributing

Contributions are welcome! If you'd like to contribute to either of these projects, please follow the guidelines outlined in the respective repositories.

## License

Both AT-Conv-LSTM and deeprl_signal_control projects are licensed under the [MIT License](LICENSE).
