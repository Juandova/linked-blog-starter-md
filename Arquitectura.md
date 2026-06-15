---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre
Asignatura:
  - Enjambre
date: 2026-05-30
---
``` title:Arquitectura
                +-------------------+
                | QGroundControl    |
                | (Ground Station)  |
                +---------+---------+
                          |
                       MAVLink
                          |
                +---------v---------+
                | PX4 Autopilot     |
                | (FCU / SITL)      |
                +---------+---------+
                          |
                    uXRCE-DDS
                          |
                +---------v---------+
                | ROS 2             |
                | Algoritmos        |
                | IA / Swarm        |
                +---------+---------+
                          |
                    Sensores
                    Visión
                    Planificación
```

donde: 
- **[[PX4]]** → controla el vuelo.
- **[[QGroundControl]]** → configura y monitoriza drones.
- **[[ROS 2]]** → lógica avanzada, IA, navegación, coordinación de enjambres.
- **[[Gazebo]]** → simulación.
- **[[MAVLink]]** → protocolo de comunicación.
- **[[DDS]]/[[uXRCE-DDS**]] → puente [[ROS 2]] ↔ [[PX4]].

