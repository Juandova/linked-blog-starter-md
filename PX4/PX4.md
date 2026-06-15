---
tags:
  - MASTER/MUSANTTA
  - drones/autopilot/PX4
date: 2026-05-11
---
> [!summary] 
> **PX4** es una **plataforma _open-source_ de piloto automático** para vehículos no tripulados. Proporciona el software encargado del control de vuelo, estimación del estado, planificación básica y gestión de sensores y actuadores.


> [!hint] Arquitectura modular
> Su arquitectura modular permite ejecutarlo tanto sobre hardware real como en entornos de simulación, integrándose además con ecosistemas como [[ROS 2|ROS 2]] para el desarrollo de aplicaciones robóticas avanzadas.

### Documentación

- [PX4](https://px4.io/)
- [PX4-Autopilot Github](https://github.com/px4/px4-autopilot/)
- [PX4 Autopilot User Guide](https://docs.px4.io/main/en/)
- [ROS 2 User Guide](https://docs.px4.io/main/en/ros2/user_guide)

### "*Instalación* " y compilación 

```sh title:"Descarga de repositorio"
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot
```

```sh title:"Compilar"
make px4_sitl
```


### Ejecución

```sh  title:"Ejecución"
cd ~\PX4-Autopilot
PX4_HOME_LAT=39.48053 PX4_HOME_LON=-0.33928 PX4_HOME_ALT=10 make px4_sitl gz_x500
```

> [!success]  Se ejecuta el autopilot virtual en entorno de simulación de [[Gazebo]]
> Además, mediante las variables de entorno `PX4_HOME_LAT`, `PX4_HOME_LON` y `PX4_HOME_ALT`, el origen geográfico del mundo simulado se puede asociar a una ubicación real. En este caso, el punto `(0,0)` de [[Gazebo]] se sitúa aproximadamente en la UPV.


## Vehículos Soportados

- Multicópteros
- Alas fijas
- VTOL
- Rover
- Embarcaciones (_Boat_)
- Vehículos submarinos experimentales

## Compatibilidades

- [[uORB]]: bus interno de publicación/suscripción utilizado para la comunicación entre módulos de PX4.
- [[DDS]]: middleware orientado a sistemas distribuidos que permite la interoperabilidad mediante el estándar _Data Distribution Service_.
- [[ROS 2]]: integración mediante `px4_ros_com` y `micro XRCE-DDS`, facilitando el intercambio de datos entre PX4 y nodos ROS 2.
- [[Gazebo]]: simulación _Software-In-The-Loop_ ([[SITL]]) para validar algoritmos sin necesidad de hardware físico.
- [[QGroundControl]]: estación de control en tierra para configuración, monitorización y planificación de misiones.

