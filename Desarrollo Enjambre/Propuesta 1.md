---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre/ROS
date: 2026-06-16
---



```
                  swarm_manager
                        │
        ┌───────────────┼────────────────┐
        │               │                │
    drone_1         drone_2          drone_3
 swarm_agent     swarm_agent      swarm_agent
        │               │                │
       PX4             PX4              PX4
```


```sh title:"Ejecución"
ros2 run swarm_pkg swarm_agent_node --ros-args -p drone_id:=0
```


```sh title:"Prueba de ejecución"
ros2 topic pub --once /px4_swarm/command std_msgs/msg/String "{data: TAKEOFF}"
```



---
## hoja de ruta:

### Fase 1

- [x]  [[Launch enjambre]]


---
### Fase 2

- [ ] Crear `swarm_agent`.

Una copia reducida de tu `manual_control_node`:

- arm
- disarm
- offboard
- takeoff
- land

por namespace.

---

### Fase 3

- [ ] Crear `swarm_manager`.

Comandos:

```
armtakeoffland
```

para todos.

---

### Fase 4

Mover todos:

```
/swarm/cmd_vel
```

---

### Fase 5

Mover uno o todos:

```
selected_id
```

---

### Fase 6

Líder-seguidor.

---

### Fase 7

Formaciones.