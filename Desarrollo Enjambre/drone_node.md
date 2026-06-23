---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre
date: 2026-06-17
---
> [!summary] Nodo con la responsabilidad de controlar cada dron de forma individual. 
> Recibiendo las intrucciones de control del enjambre




```
                swarm_manager_node
                        │
        ┌───────────────┼────────────────┐
        │               │                │
	drone_1         drone_2          drone_3
	drone_node      drone_node       drone_node
        │               │                │
       PX4             PX4              PX4
```


## Ejecución

```sh title:"Ejecución"
ros2 run swarm_pkg drone_node --ros-args -p drone_id:=0
```

```sh title:"Prueba de ejecución de 3 drones"
ros2 action send_goal /drone_0/action/takeoff swarm_pkg/action/Takeoff "{altitude: 2.0}" &
ros2 action send_goal /drone_1/action/takeoff swarm_pkg/action/Takeoff "{altitude: 2.0}" &
ros2 action send_goal /drone_2/action/takeoff swarm_pkg/action/Takeoff "{altitude: 2.0}" &
wait
```

```sh
ros2 action send_goal /drone_0/action/land swarm_pkg/action/Land "{}" &
ros2 action send_goal /drone_1/action/land swarm_pkg/action/Land "{}" &
ros2 action send_goal /drone_2/action/land swarm_pkg/action/Land "{}" &
wait
```

```sh title:"Prueba de movimiento"
ros2 topic pub --once /drone_0/in/target_pose geometry_msgs/msg/PoseStamped "{pose: {position: {x: 5.0, y: 0.0, z: -9.0}}}"
```

> [!warning]  Ojo
> PX4 está usando el sistema de coordenadas **NED** (_North-East-Down_).

```sh title:"Prueba de rotación"
ros2 topic pub --once /drone_0/in/target_yaw std_msgs/msg/Float32 "{data: 3.14}" &
ros2 topic pub --once /drone_1/in/target_yaw std_msgs/msg/Float32 "{data: 3.14}" &
ros2 topic pub --once /drone_2/in/target_yaw std_msgs/msg/Float32 "{data: 3.14}" &
wait
```


---
## Topics

prefix = `px4_0/fmu/`  (en función del dron)

### Publisher

- prefix + `/in/offboard_control_mode`

- prefix + `/in/trajectory_setpoint`

 - prefix + `/in/vehicle_command`

### subscription

- `/px4_swarm/command`

- prefix + `/out/vehicle_status_v4`

- prefix + `/out/vehicle_local_position_v1`

- prefix + `/out/vehicle_odometry`

- prefix + `/out/vehicle_land_detected`

- prefix + `/out/vehicle_command_ack_v1`


---
### Topics creados:
> [!success]  Resultado con 3 drones: 

```
/drone_0/in/target_pose
/drone_0/out/pose
/drone_0/action/takeoff
/drone_0/action/land

/drone_1/in/target_pose
/drone_1/out/pose
/drone_1/action/takeoff
/drone_1/action/land

/drone_2/in/target_pose
/drone_2/out/pose
/drone_2/action/takeoff
/drone_2/action/land
```


---

## Responsabilidad

El `drone_node` es la capa de abstracción entre el sistema de enjambre y PX4.

Su función es ocultar todos los detalles internos de PX4 (topics FMU, mensajes específicos, modos de vuelo, comandos MAVLink, sistema NED, etc.) y exponer una interfaz ROS2 sencilla basada en:

- Actions para órdenes discretas.
    
- Topics para consignas continuas.
    
- Telemetría simplificada del estado del dron.
    

Cada instancia de `drone_node` controla un único vehículo PX4.

Por ejemplo:

```
drone_0 -> PX4 instancia 0
drone_1 -> PX4 instancia 1
drone_2 -> PX4 instancia 2
```

De esta forma, los nodos de nivel superior (`manual_swarm_control`, `swarm_manager`, algoritmos de formación, evitación de colisiones, etc.) no necesitan conocer detalles de PX4.

---

## Arquitectura

```
	            swarm_manager_node
                       │
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
   drone_0         drone_1         drone_2
   drone_node      drone_node      drone_node
       │               │               │
       ▼               ▼               ▼
      PX4             PX4             PX4
```

---

## Interfaz

### Actions

Operaciones puntuales:

```
/drone_N/action/takeoff
/drone_N/action/land
```

### Topics de entrada

Consignas de movimiento:

```
/drone_N/in/target_pose
```

Tipo:

```
swarm_pkg/msg/DronePose
```

```
x
y
z
yaw
```

### Topics de salida

Estado simplificado del vehículo:

```
/drone_N/out/pose
```

Tipo:

```
swarm_pkg/msg/DronePose
```

```text
x
y
z
yaw
```

---

## Traducción de responsabilidades

El `drone_node` traduce:

```
Takeoff Action
        ↓
VehicleCommand PX4

Land Action
        ↓
VehicleCommand PX4

DronePose
        ↓
TrajectorySetpoint

VehicleOdometry
        ↓
DronePose
```

---

## Filosofía de diseño

El resto del enjambre nunca debería publicar directamente sobre:

```
/px4_x/fmu/in/*
```

ni subscribirse a:

```
/px4_x/fmu/out/*
```

Toda interacción con PX4 debe realizarse a través de `drone_node`.