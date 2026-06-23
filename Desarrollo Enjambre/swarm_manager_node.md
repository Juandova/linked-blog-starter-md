---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre/ROS
date: 2026-06-23
---












---

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