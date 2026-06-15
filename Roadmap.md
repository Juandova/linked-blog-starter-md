---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre
Asignatura:
  - Enjambre
date: 2026-05-30
---
> [!summary] 
>  **Objetivo final**
>  Desarrollar y controlar **enjambres de drones (swarms)** utilizando:
>  - [PX4 Autopilot](https://px4.io/)
>  - [ROS 2](https://docs.ros.org/en/humble/index.html)
>  - [QGroundControl](https://qgroundcontrol.com/)

```  title:"Roadmap Resumido"
Linux 
        ↓
ROS2 Básico
        ↓
ROS2 Avanzado
        ↓
PX4
        ↓
QGroundControl
        ↓
PX4 + ROS2
        ↓
Offboard Control
        ↓
Navegación Autónoma
        ↓
2 Drones
        ↓
5 Drones
        ↓
Formaciones
        ↓
¿Swarm Intelligence? (opcional)
        ↓
Hardware Real
```

# Fase 0 — Fundamentos

![[Arquitectura]]

---
# Fase 1 — Aprender ROS2 

Instala:
- Ubuntu 22.04
- ROS2 Humble

[[PX4]] recomienda [[ROS 2]] Humble como entorno principal.

## Qué aprender

### Nivel básico

- [ ] Nodes
- [ ] Topics
- [ ] Publishers
- [ ] Subscribers
- [ ] Services
- [ ] Actions

### Nivel medio

- [ ] QoS
- [ ] TF2
- [ ] Launch files
- [ ] Parameters

### Nivel avanzado

- [ ] Lifecycle Nodes
- [ ] [[DDS]]
- [ ] Multi-robot systems

---
### Cursos oficiales

- [ROS 2 Documentation](https://docs.ros.org/en/humble/index.html?utm_source=chatgpt.com)
- [ROS Tutorials](https://docs.ros.org/en/humble/Tutorials.html?utm_source=chatgpt.com)

Proyecto práctico:

Construye:

```
Nodo cámara      |Nodo detección      |Nodo navegación
```

sin drones todavía.

---
# Fase 2 — Aprender [[PX4]]

Instala:

- [[PX4]]
- [[Gazebo]]
- [[QGroundControl]]

Documentación oficial:

- [PX4 Documentation](https://docs.px4.io/main/en/?utm_source=chatgpt.com)
- [PX4 ROS2 Guide](https://docs.px4.io/main/en/ros2/user_guide?utm_source=chatgpt.com)

---
## Qué aprender

### Arquitectura interna

- [ ] [[uORB]]
- [ ] Commander
- [ ] Navigator
- [ ] Estimators
- [ ] Flight Modes

### Sensores

- [ ] [[IMU]]
- [ ] [[GNSS]]
- [ ] Barómetro
- [ ] Magnetómetro

### Control

- [ ] Rate Control
- [ ] Attitude Control
- [ ] Position Control

---
## Simulación

Ejecuta:

```sh
cd ~\PX4-Autopilot
make px4_sitl gz_x500
```

---
# Fase 3 — Aprender [[QGroundControl]]

> [!info]  Conexión entre QGroundControl y dron x500 con Pixwack C6
> *desde Windows con WSL*

### Configuración

- [ ] Calibrar sensores
- [ ] Calibrar RC
	- [ ] Importante saber cómo hacer el Handover
- [ ] Configurar modos

### Telemetría

- [ ] Revisar estado
- [ ] Logs
	- [ ] Mirar logs automáticos
- [ ] Health checks

### Misiones

- [ ] Waypoints
- [ ] [Survey missions](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/plan_view/pattern_survey.html)
	- generate an autonomous grid flight pattern over a designated polygonal area
- [ ] [Geofence](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/plan_view/plan_geofence.html)

Sitio oficial:
- [QGroundControl](https://qgroundcontrol.com/?utm_source=chatgpt.com)

> [!success]  Conexión entre QGroundControl y dron x500 con Pixwack C6
> *desde Linux*

---
# Fase 4 — Conectar [[ROS 2]] con [[PX4]] 

[[PX4]] utiliza actualmente:

```
ROS2  |uXRCE-DDS Agent  |PX4
```

Aprende:
- [[px4_msgs]]
- px4_ros_com
- Offboard Control

---
Primer proyecto:

```
ROS2 Node      |Envía setpoints      |PX4      |Drone despega
```

Documentación:
- [PX4 ROS2 User Guide](https://docs.px4.io/main/en/ros2/user_guide)

Vídeo: [ROS World 2020: Getting started with ROS 2 and PX4](https://www.youtube.com/watch?v=qhLATrkA_Gw&t=6s)

---
### Comandos:

```sh title:"Inicializador 1º dron"
cd ~/PX4-Autopilot
PX4_HOME_LAT=39.48053 PX4_HOME_LON=-0.33928 PX4_HOME_ALT=10 make px4_sitl gz_x500
```

```sh title:"Iniciar QGroundControl"
cd ~
./QGroundControl-x86_64.AppImage
```

##### crear la comunicación ROS- PX4

```sh title:"Abrir microagente"
MicroXRCEAgent udp4 -p 8888
```

Instalar: [[px4_msgs]]

```sh title:"px4_msgs"
cd ~/utiles_px4_ws/
colcon build
source install/setup.bash
```

ver [[topic comands]]

> [!success]  Conseguido
```
Gazebo
   ↓
PX4 SITL
   ↓ uORB
MicroXRCEAgent
   ↓ DDS
ROS2
```

---
# Fase 5 — Control

> [!info] Objetivo:
> Un único dron autónomo.

- Instalar Visual Code Studio
	- Luego instala estas extensiones:
		- C/C++
		- CMake Tools
		- ROS
		- Error Lens (opcional pero útil)
		- 

---
 > [!todo] Ver
 >-> [[Crear paquete ROS2]] 
 
[[Toma de contacto ROS2]] : Se crea un workspace para testear conceptos:
``` title:"Estructura del workspace"
test_px4_ros_ws/
│
├── src/
│   └── px4_test_cpp/
│       ├── src/
|		|	├──	vehicle_position_listener.cpp
│       │   ├── arm_node.cpp
│       │   ├── takeoff_node.cpp
|		|	├──	land_node.cpp
│       │   └── offboard_node.cpp
|		|	└── move_forward.cpp
│       │
│       ├── CMakeLists.txt
│       └── package.xml
│
├── build/
├── install/
└── log/
```


> [!todo]  Separar en carpetas los nodos de escucha y los de ordenes

---
### Entender:

> [!info]  Para ver la estructura del msg
```sh
ros2 interface proto px4_msgs/msg/VehicleCommand
```


> [!info]  Para ver el tipo de contenido del msg
```sh
ros2 interface show px4_msgs/msg/VehicleCommand
```

> [!example] Resultados interesantes: 
- `uint16 VEHICLE_CMD_COMPONENT_ARM_DISARM = 400 # Arms / Disarms a component. |1 to arm, 0 to disarm.`
	- estás mandando:
		- `command = 400`
		- `param1 = 1` para armar, o `0` para desarmar

- `uint16 VEHICLE_CMD_NAV_TAKEOFF = 22 # Takeoff from ground / hand. |Unused (FW pitch from FW_TKO_PITCH_MIN)|Unused|Unused|[deg] [@range 0,360] Yaw angle in NED if yaw source available, ignored otherwise|Latitude (WGS-84)|Longitude (WGS-84)|[m] Altitude AMSL|`
	- está mandando: 
		- `command = 22`
		- `param4 -> yaw`
		- `param5 -> latitude `
		- `param6 -> longitude`
		- `param7 -> altitude AMSL`

- `uint16 VEHICLE_CMD_NAV_RETURN_TO_LAUNCH = 20 # Return to launch location. |Unused|Unused|Unused|Unused|Unused|Unused|Unused|`
	- envía solo `command = 20`
		- *no hace falta enviar nada más*

- `uint16 VEHICLE_CMD_NAV_LAND = 21 # Land at location. |Unused|Unused|Unused|Desired yaw angle.|Latitude|Longitude|Altitude|`
	- manda: 
		- `command = 21`
		- `param4 -> yaw`
		- `param5 -> latitud`
		- `param6 -> longitud`
		- `param7 -> altitud`
`


---
### Investigar
#### Percepción

- [ ] OpenCV
- [ ] [[YOLO]]

##### Evitación de obstáculos

- [ ] [VFH](https://www.sciencedirect.com/science/article/pii/S0360835223007854)
#### Mapping

- [ ] RTABMap
- [ ] Octomap

#### Planning

- [ ] Nav2
- [ ] A*

#### Control

- Offboard Mode

![[topic comands#Entrar en modo Offboard]]

%%---

Proyecto:

```
Buscar objetoDetectarloNavegarAterrizar
```
%%

---

# Fase 6 — Multi-UAV 

> [!summary]  Empezar a simular más de uno dron
> Empezar a manejar varios drones

---
### Namespaces ROS2

> [!important]  La gestión de namespaces es uno de los problemas más comentados cuando se escala PX4+ROS2 a varios UAV.

porque cada vehículo debe tener sus propios topics.

```  title:Ejemplo
/uav1
/uav2
```

---
 ![[Launch enjambre#Ejecución]]

---
### Formación enjambre

Implementa:
- [ ] Leader-Follower
- [ ] Formation Control


```  title:Ejemplo
Leader  |  +---- Follower 1  |  +---- Follower 2
```

---
# Fase 7 - Formaciones dinámicas

#completar 

---
# Fase 8 - ¿Enjambres Heterogéneos?


---
# Fase 9 — ¿Enjambre inteligente?

### Algoritmos clásicos

- Reynolds Boids
- Vicsek
- Consensus Algorithms

### Multi-Agent Systems

- Distributed Control
- Auction Based Planning
- Task Allocation

### SLAM colaborativo

- Multi-Robot SLAM

### Reinforcement Learning

- MADDPG
- MAPPO

---

Lecturas interesantes:

El paper de arquitectura ROS2+PX4 para enjambres es especialmente relevante porque ya aborda:

- formación
- seguimiento de líder
- coordinación distribuida
- integración de estación de tierra

---
# Fase 10 — Hardware real

### Flight Controller

- Holybro Pixhawk 6C

### Companion Computer

- NVIDIA Jetson Orin Nano

### Telemetría

- [[SiK Radio]]
- [[WiFi]] Mesh
- LTE/[[5G]]
- Conexión ESP32-I2C

