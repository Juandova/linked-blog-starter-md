---
tags:
  - drones/enjambre
  - drones/autopilot/PX4
date: 2026-06-04
---
> [!summary]  
> Recopilación de comandos utilizados habitualmente durante el desarrollo, simulación e integración de [[PX4]] con [[Gazebo]], [[ROS2]] y [[QGroundControl]].

---
## SITL con Gazebo

### Ejecutar simulación básica

```sh
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

---
### Ejecutar simulación con origen geográfico

```sh
cd ~/PX4-Autopilot
PX4_HOME_LAT=39.48053 PX4_HOME_LON=-0.33928 PX4_HOME_ALT=10 make px4_sitl gz_x500
```


> [!info]  
> Sitúa el origen `(0,0)` del mundo de [[Gazebo]] aproximadamente en la UPV.


---
### Cargar un mundo concreto

```sh
PX4_GZ_WORLD=windy make px4_sitl gz_x500
```

Otros mundos disponibles:

```sh
PX4_GZ_WORLD=baylands make px4_sitl gz_x500
PX4_GZ_WORLD=default make px4_sitl gz_x500
```

---
### Ejecutar otro modelo de vehículo

ver: [Gazebo Vehicles](https://docs.px4.io/main/en/sim_gazebo_gz/vehicles#x500-quadrotor)

```sh
make px4_sitl gz_iris
```

```sh
make px4_sitl gz_x500
```

```sh
make px4_sitl gz_standard_vtol
```

### [[PX4_SYS_AUTOSTART]]

```sh title:"ejemplo de uso"
PX4_SYS_AUTOSTART=4001 PX4_GZ_MODEL=gz_x500 ./build/px4_sitl_default/bin/px4
```

### Compilación

#### Compilar SITL

```sh
make px4_sitl
```

---
#### Limpiar compilación

```sh
make clean
```

---
#### Limpiar completamente

```sh
make distclean
```

> [!warning]  
> Elimina configuraciones generadas y fuerza una recompilación completa.

---
## Consola PX4

### Abrir la consola MAVLink

Una vez lanzado PX4:

```sh
pxh>
```

permite ejecutar comandos internos del autopiloto.

Ejemplos:

---
### Mostrar ayuda

```sh
help
```

---

### Listar aplicaciones disponibles

```sh
?
```

o

```sh
help
```

---
### Ver Topics [[uORB]] publicados

```sh
listener vehicle_status
```

```sh
listener vehicle_attitude
```

```sh
listener sensor_combined
```

---
%% ### Mostrar información de sensores

```sh
sensors status
```

---
### Estado del estimador

```sh
ekf2 status
```

---
### Mostrar parámetros

```sh
param show
```

---
### Buscar un parámetro

```sh
param show COM_ARM*
```

---

## Logs

### Mostrar información de logs

```sh
logger status
```

---

### Iniciar logger

```sh
logger on
```

---

### Detener logger

```sh
logger off
```

---
%%
## uXRCE-DDS

### Ejecutar el Agent

```sh
MicroXRCEAgent udp4 -p 8888
```

---

### Verificar que PX4 está publicando

En ROS 2:

```sh
ros2 topic list
```

---

### Escuchar un Topic

```sh
ros2 topic echo /fmu/out/vehicle_status
```

---

## ROS 2

### Listar Topics

```sh
ros2 topic list
```

---

### Mostrar información de un Topic

```sh
ros2 topic info /fmu/out/vehicle_status
```

---

### Mostrar mensajes

```sh
ros2 topic echo /fmu/out/vehicle_attitude
```

---
### Mostrar frecuencia de Topics

```sh
ros2 topic hz /fmu/out/vehicle_odometry
```

---
### Listar nodos

```sh
ros2 node list
```

---
### Mostrar estructura del mensaje

```sh 
ros2 interface proto <topic>
```

```sh
ros2 interface show px4_msgs/msg/VehicleCommand
```




## QGroundControl

### Conexión automática

Al ejecutar:

```sh
make px4_sitl gz_x500
```

QGroundControl suele conectarse automáticamente mediante MAVLink.

---

### Reiniciar parámetros

Desde [[QGroundControl]]:

```
Vehicle Setup
→ Parameters
→ Tools
→ Reset to defaults
```

---
## Referencias rápidas

[[PX4]]  
[[Gazebo]]  
[[SITL]]  
[[uORB]]  
[[ROS 2]]  
[[Micro XRCE-DDS]]  
[[px4-uxrce_dds_client]]  
[[QGroundControl]]