---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/autopilot/PX4
date: 2026-06-15
---

> [!success]  Ricardo lo ha conseguido
> ¿Cómo? ª


##  Hipótesis: 

#### Por ejecutar PX4 con [[PX4_SYS_AUTOSTART]]

> [!failure] Sigue pidiendo [[QGroundControl]]

#### Por ejecutar [[micro ROS Agent]]

en vez de usar [[Micro XRCE-DDS]] solo con: 
```sh 
MicroXRCEAgent udp4 -p 8888
```

> [!note]  entonces, puede que le esté corriendo un servicio que le permita completar el checklist por detrás, y por ende le permite armar el dron

> [!failure]  Al ejecutar con `micro-ros-agent udp4 --port 8888`  sigue pidiendo [[QGroundControl]]


