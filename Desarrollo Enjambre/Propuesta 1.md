---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre/ROS
date: 2026-06-16
---



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


```sh title:"Ejecución"
ros2 run swarm_pkg drone_node --ros-args -p drone_id:=0
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

- [x] Crear [[drone_node]].

Una copia reducida de tu `manual_control_node`:

- arm
- disarm
- offboard
- takeoff
- land

por namespace.

- [ ] Ampliar [[drone_node]] para control de posición

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