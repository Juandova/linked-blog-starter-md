---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre/ROS
date: 2026-06-23
---
> [!summary] responsabilidad
> Indicar cómo se tiene que mover el centroide

```
ros2 run swarm_pkg swarm_command_node
```

## topics

## responsabilidades

> [!example]  Mover el centroide

Ya sea con control por teclas (o mando) o por waypoints desde [[Mission_planner]]


## estructura

```
SwarmCommandNode
│
├── Subscriber ¿?
│      /swarm/out/pose
│
├── Publisher
│      /swarm/in/target_pose
│
├── Publisher
│      /swarm/in/command
│
├── Keyboard
│
├── move_relative()
├── rotate_relative()
├── stop_motion()
├── send_takeoff()
├── send_land()
├── handle_key()
├── read_key()
├── enable_raw_mode()
└── disable_raw_mode()
```


```
Teclado
      │
      ▼
swarm_command
      │
      ├── /swarm/in/target_pose
      └── /swarm/in/command
               │
               ▼
        swarm_manager
               │
      ┌────────┴────────┐
      ▼                 ▼
Takeoff/Land      Target_Pose
```