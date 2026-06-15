---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre
date: 2026-06-12
---
> [!summary] 
> Un **Workspace** de [[ROS2]] es un directorio que agrupa uno o varios paquetes ROS 2 junto con los artefactos generados durante su compilación. Constituye la unidad básica de desarrollo en ROS 2, permitiendo construir, instalar y ejecutar aplicaciones robóticas de forma aislada del resto del sistema.



![[Crear paquete ROS2#Crear paquete ROS 2]]

## Estructura típica

Un Workspace ROS 2 suele tener la siguiente organización:

```
<workspace>/
│
├── src/
├── build/
├── install/
└── log/
```

###### Ejemplo WorSpace

``` title:"Estructura del workspace"
test_px4_ros_ws/
│
├── src/
│   └── px4_test_pkg_cpp/
│       ├── src/
|		|	├──	vehicle_position_listener.cpp
│       │   ├── arm_node.cpp
│       │   ├── takeoff_node.cpp
|		|	├──	land_node.cpp
│       │   └── offboard_node.cpp
|		|	└── move_forward.cpp
│       │
│       ├── CMakeLists.txt
│       └── package.xml
│
├── build/
├── install/
└── log/
```

## Compilación

Desde la raíz del Workspace:

```sh
colcon build
```

#### Compilar un único paquete:

```sh
colcon build --packages-select <nombre_paquete>
```

#### Compilar utilizando enlaces simbólicos:

```sh
colcon build --symlink-install
```

> [!success]  
> `--symlink-install` evita copiar archivos Python y recursos, facilitando el desarrollo iterativo.

## Cargar el entorno

Tras cada compilación (desde la raíz del Workspace):
```sh
source install/setup.bash
```

Puede añadirse al `.bashrc` si el Workspace se utiliza habitualmente. Ver: [[Bashrc - carga automática]]

---
