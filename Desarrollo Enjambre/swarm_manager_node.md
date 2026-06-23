---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre/ROS
date: 2026-06-23
---
> [!summary]  Responsabilidad:
> En base a [[Formación node]] y [[swarm_command_node]] calcula la posición de cada dron y manda instrucciones de movimiento a [[drone_node]]


### Ejecución

```sh title:"Prueba de ejecución"
ros2 run swarm_pkg swarm_manager_node --ros-args -p num_drones:=3
```

```sh title:"Prueba de ejecución"
ros2 topic pub --once /swarm/target_pose swarm_pkg/msg/DronePose "{x: 0.0, y: 0.0, z: -2.0, yaw: 0.0}"
```
## topics

#### suscribe

`/swarm/target_pose`

`drone_N/formacion`

#### publica

`/drone_N/in/target_pose`

## Responsabilidades 


Recibe:

```
offsets de formación
 +
estado del centroide
```

y calcula:

```
posición individual de cada dron
```





---
%% ¿pa borrar?
###### Propuesta Chaty:
Ahora que ya tienes Action funcionando, puedes implementar un patrón mucho mejor para el enjambre:

```
SwarmTakeoff.action
```

en el `swarm_manager_node`.

Por ejemplo:

```
float32 altitude---bool success---uint32 completed_dronesuint32 total_drones
```

Cuando alguien haga:

```
ros2 action send_goal /swarm/takeoff swarm_pkg/action/SwarmTakeoff "{altitude: 2.0}"
```

el manager:

1. Envía simultáneamente goals a los 9 drones.
2. Espera a que los 9 respondan.
3. Devuelve SUCCESS sólo cuando todos hayan terminado.

Esa arquitectura suele ser la más limpia para enjambres porque desacopla:

```
Operador    ↓Swarm Manager    ↓Drone Actions
```

y evita tener que lanzar 9 comandos manualmente cada vez. Ahora que has conseguido que un `drone_node` funcione como servidor Action, ya tienes prácticamente resuelto el bloque más difícil.

%%