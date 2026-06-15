---
tags:
  - drones/enjambre/ROS
---
> [!summary]  Protocolo de comunicación publiser-subcritor
> #completar 
## Instalación

```sh
git clone --recursive https://github.com/eProsima/Fast-DDS.git
cd Fast-DDS
mkdir build && cd build
cmake ..
make
sudo make install
```


> [!failure]  Error: al ejecutar make
> - versión de Fast-DDS: 2.10.1.
> - versión [[ROS Humble]] [[Fast-CDR]]: 1.0.29
> 
> existen en versiones más modernas de Fast-CDR que la 1.0.29 que trae ROS Humble

> [!todo]  Solución
> manos de Ricardo
> - Usar Fast-DDS: 2.1.1
> 	- con `git checkout v2.1.1`

```sh
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
```



[[DDS]]