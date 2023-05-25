# TOD-simulator
ToD-Simulator is a simulation environment for the TeleOperatedDriving service. It consists of two key components: `tod-carla`, which is an extension of the CARLA simulator used to simulate the inter-vehicular system, and `tod-omnet`, which uses OMNeT++ to simulate the network system. Communication between the two simulators is handled by the open-source library [CARLANeT](https://github.com/carlanet), which ensures consistent co-simulation.
<p align="center">
 <img src="https://github.com/connets/tod-simulator/blob/dev/images/tod-simulator_structure.png" alt>
</p>
<p align="center">
 <em>Overview of ToD-simulator architecture</em>
</p>

Other than the two components mentioned above, there is a third component that contains the CARLA simulator. This component is provisioned with a controller and a supervisor to simplify communication and avoid crashing bugs in the simulator. For more information on this component, refer to the documentation in the directory.

To run the simulator, it is highly recommended to use Docker Compose, a tool that handles different dependencies and communication between the various parts. Docker Compose offers flexibility, allowing you to run the components on different hosts and simplifying communication-related issues.

## Prerequisites
- git 1.8.2+
- Docker
- Docker Compose v1.28.0+ 
- NVIDIA Container Toolkit

## Installation
To get started, clone the TOD-simulator repository and update the submodules:
```sh
git clone https://github.com/connets/tod-simulator --recurse-submodules && cd tod-simulator && git submodule update --recursive --remote
```

# Customizing ToD simulation Setup
To customize the ToD simulation setup, refer to the [`tod-omnet`](https://github.com/connets/tod-omnet) and [`tod-carla`](https://github.com/connets/tod-carla) repositories. Note that to customize the arguments for `tod-carla`, the .env file contains the parameter `SIMULATOR_CONFIGURATION_FILE_PATH`, which specifies the relative path (starting from tod-carla root) of the server configuration file path. `TOD_CARLA_ARGS` variable contains all the optional arguments for the tod-carla simulator. Refer to the specific repository for more information.

For customization of tod-omnet, you need to modify the Dockerfile in the specific repository. A better solution for this customization will be provided in the future.

## Docker Compose Profiles

Docker Compose provides profiles for different scenarios:
   - `on-board-driver`: Runs the TOD-Simulator with the agent inside the vehicle, without any delays in the communication.
   - `remote-driver`: Runs the TOD-Simulator with the agent located remotely, using `tod-omnet` as the simulator for the communication network.
   - `within-carla-sim`: Runs the CARLA simulator as part of the Docker Compose setup. This is recommended to avoid configuration issues.
Please note that the `on-board-driver` and `remote-driver` profiles are mutually exclusive, so you must choose only one of them based on your requirements.

## Usage
To run the TOD-Simulator with an on-board driver, execute the following commands:

```sh
docker compose --profile on-board-driver --profile within-carla-sim build
docker compose --profile on-board-driver --profile within-carla-sim up
```


To run the TOD-Simulator with a remote driver using tod-omnet, execute the following commands:
```sh
docker compose --profile remote-driver --profile within-carla-sim build
docker compose --profile remote-driver --profile within-carla-sim up
```

After the simulation is completed, you can access the results in the `results` folder. The `results` folder contains subdirectories for vehicular and network results, corresponding to the CARLA and OMNeT simulations, respectively. Each subdirectory corresponds to a simulation ID.


## Note for Windows Users

Please note that there are some known issues with `within-carla-sim` profile due to bugs in the CARLA simulator image. As a result, running the TOD-Simulator on a Windows environment using this profile is not recommended.

To run the TOD-Simulator in a Windows environment, you need to run CARLA simulator (with the controller and supervisor) directly on your local machine without using Docker. Refer to the [documentation](https://github.com/connets/tod-simulator/tree/dev/carla-sim-supervisor) of `carla-sim-supervisor` for instructions on running CARLA locally.

After running CARLA on your local machine, you'll need to modify the environment variable `TOD_CARLA_ARGS` by adding a custom configuration for the CARLA server's host and port. Here's an example of how to configure it:
```sh
TOD_CARLA_ARGS = "--carla_server.host 192.168.1.10 --carla_server.carla_simulator_port 2000"
```

Make sure to replace `192.168.1.10` with the actual IP address of your CARLA server, and `2000` with the corresponding port number. This configuration allows the TOD-Simulator to establish a connection with the locally running CARLA simulator.

Once you have set up and run `carla-sim-supervisor` on a machine, and modified the `TOD_CARLA_ARGS` environment variable to include the IP address of the host running the CARLA simulator, you are ready to run the simulation using Docker Compose. For example, to run the simulation with the `remote-driver` profile using `tod-omnet`, execute the following commands:

```sh
docker compose --profile remote-driver build
docker compose --profile remote-driver up
```

Please note that this workaround is specific to Windows environments and is required to address the limitations and issues related to running CARLA within Docker on Windows.

## License
ToD-Simulator is distributed under the MIT License. See LICENSE for more information.
