# TOD_simulator_compose
## Prerequisites
- git 1.8.2+
- Docker
- Docker Compose v1.28.0+ 
- NVIDIA Container Toolkit
## Installation
```sh
git clone https://github.com/Jaivra/tod_simulator_compose --recurse-submodules
git submodule update --recursive --remote
```
if you want to run it with omnet network for communication:
```sh
docker-compose --profile zero_delay_network build
docker-compose --profile zero_delay_network up 
```
if you want to run it without any delays applied to the messages between vehicle and operator (in-vehicle user):
```sh
docker-compose --profile zero_delay_network build
docker-compose --profile zero_delay_network up 
```
