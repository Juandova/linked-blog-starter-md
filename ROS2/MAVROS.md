---
tags:
  - drones/enjambre
  - MASTER/MUSANTTA/Practicas
date: 2026-06-18
---
[mavros](https://docs.ros.org/en/humble/p/mavros/)

921600

115200

## Installation

```sh title:"Instalación MAVROS"
sudo apt update
sudo apt install -y ros-humble-mavros ros-humble-mavros-extras geographiclib-tools
```

Luego instala los datasets de GeographicLib::

```sh 
source /opt/ros/humble/setup.bash
sudo bash /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh
```

## Lanzar

```sh 
ros2 launch mavros px4.launch fcu_url:=/dev/ttyUSB0:57600 gcs_url:=udp://@127.0.0.1:14550
```

## Complobar

```sh
ros2 topic list | grep mavros
```