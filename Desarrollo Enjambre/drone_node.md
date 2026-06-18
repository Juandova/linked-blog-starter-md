---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre
date: 2026-06-17
---
> [!summary] Nodo con la responsabilidad de controlar cada dron de forma individual. Recibiendo las intrucciones de control del enjambre




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


```sh title:"Prueba de ejecución"
ros2 topic pub --once /px4_swarm/command std_msgs/msg/String "{data: TAKEOFF}"
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


