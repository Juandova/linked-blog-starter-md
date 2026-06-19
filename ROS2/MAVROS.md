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

## Comprobar

```sh
ros2 topic list | grep mavros
```


---




---

> [!failure] Frecuencia de mensajes parece capada de serie dando 1 Hz
```sh 
ros2 service call /mavros/set_message_interval mavros_msgs/srv/MessageInterval "{message_id: 32, message_rate: 30.0}"
```


---
## flujo

``` 
Pixhawk TELEM1
	↓ MAVLink por radio
Antena USB PC /dev/ttyUSB0
	↓
MAVROS
	├──	ROS 2 topics: /mavros/...
	└── UDP 14550 → QGroundControl
```

