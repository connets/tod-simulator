# TOD-simulator
ToD-Simulator is a simulation environment for the TeleOperatedDriving service. It consists of two key components: tod-carla, which is an extension of the CARLA simulator used to simulate the inter-vehicular system, and tod-omnet, which uses OMNeT++ to simulate the network system. Communication between the two simulators is handled by the open-source library [CARLANeT](https://github.com/carlanet), which ensures consistent co-simulation.

## Prerequisites
- git 1.8.2+
- Docker
- Docker Compose v1.28.0+ 
- NVIDIA Container Toolkit
## Installation
```sh
git clone https://github.com/connets/tod_simulator_compose --recurse-submodules
git submodule update --recursive --remote
```

## Customizing the TOD Simulation Setup
To customize the TOD simulation setup, refer to the tod_omnet_network and tod_simulator repositories.


## Usage
To run the simulator, use docker compose, which allows you to launch all simulation components on a single machine or across multiple machines.

To run the application with OMNeT Simulator for communication and simulate message delays between vehicles and operators, execute the following Docker Compose commands with the **\`omnet_network\`** profile:

```sh
docker compose --profile omnet_network build
docker compose --profile omnet_network up
```
If you want to run the application without any delays applied to the messages between vehicles and operators (in-vehicle users), execute the following Docker Compose commands with the **\`zero_delay_network\`** profile:
```sh
docker-compose --profile zero_delay_network build
docker-compose --profile zero_delay_network up 
```

## Results
After the simulation is completed, you can access the results in the **\`results\`** folder. This folder contains two subdirectories for the vehicular and network results, corresponding to the Carla and OMNeT simulations respectively. You can map the results of each simulation based on the directory name, which corresponds to the simulation ID.
