# CARLA simulator supervisor

This submodule tries to overcome a well-known bug in the CARLA simulator that causes an undefined crash after resetting the world in synchronous mode. The `app.py` Python script acts as a controller for the CARLA simulator process. It provides two RPC (Remote Procedure Call) methods via ZeroRPC:

- `reload_simulator()`: Closes the CARLA simulator process, if it exists, and restarts it.

- `close_simulator()`: Terminates the CARLA simulator process, if it exists.


The `app.py` script expects one argument from the command line, which is the absolute path of `CarlaUE4.sh`, the script to run the CARLA simulator.

This repository provides a simple solution to handle the uncontrolled termination event of the CARLA simulator. A supervisor is implemented to monitor the `app.py` script, ensuring it is always running. Each time the client application (referred to as `tod-carla`) initiates a simulation, it triggers a reload of the CARLA simulator through this controller, preventing the crash.

The supervisor implementation is straightforward, consisting of a `while true` loop that continuously executes the `app.py` script using a Python command.

## Docker Usage

There are two possible solutions for using Docker with this project. The preferred option is to utilize the Docker Compose configuration provided in `tod-simulator`, which handles the communication between components (refer to the corresponding repository for the necessary commands).

The second option is to build and run this Dockerfile as a standalone module. However, it is discouraged as it does not offer significant advantages compared to the Docker Compose solution.

## Local Usage

This installation allows you to run the CARLA simulator and its associated controller/supervisor locally without using Docker. This approach is useful if you encounter difficulties running the CARLA simulator in a Docker environment, such as on Windows.

### Prerequisites

- CARLA simulator
- Python 3 or higher

### Installation

1. Install the required dependencies by running the following command:
```sh
pip install -r requirements.txt
```

2. Run the carla-simulator controller/supervisor by executing the following command:
```sh
python3 sim-controller.py *CarlaUE4.sh absolute path*
```

Replace `*CarlaUE4.sh absolute path*` with the absolute path to the `CarlaUE4.sh` script used to run the CARLA simulator.

**Note:** If you want to use this with `tod-simulator`, you must set the IP address of this machine as an environment variable in `tod-simulator`. Refer to the `tod-simulator` [documentation](https://github.com/connets/tod-simulator) for instructions on how to set the environment variable correctly.

Please note that this readme assumes you already have the CARLA simulator installed and configured properly.

Please refer to the official CARLA documentation for detailed instructions on installing and configuring the CARLA simulator environment.
