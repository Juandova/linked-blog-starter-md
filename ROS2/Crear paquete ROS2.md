---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre/ROS
date: 2026-06-08
---
> [!summary] 
> Un **paquete** es la unidad básica de distribución y reutilización en [[ROS 2]]. Contiene código fuente, ejecutables, dependencias y metadatos necesarios para construir y ejecutar funcionalidades concretas

### Crear paquete [[ROS 2]]

```sh title:"Ejemplo de crear paquete ROS2 C++"
mkdir -p ~/<NAME_ws>/src
cd ~/<NAME_ws>/src
ros2 pkg create --build-type ament_cmake --license <¿Licences?> <NAME-PKG> --dependencies rclcpp px4_msgs <¿MORE DEPENENCIAS?>
```

### Parámetros importantes

###### `--build-type`

Sistema de compilación utilizado.

Opciones habituales:

- `ament_cmake` → C++.
- `ament_python` → Python.

###### `--license`

Licencia del paquete.

Algunas opciones comunes:

- MIT
- Apache-2.0
- BSD-3-Clause
- GPL-3.0-only

###### `--dependencies`

Dependencias iniciales del paquete.

Ejemplos:

- `rclcpp`
- `rclpy`
- `px4_msgs`
- `geometry_msgs`
- `std_msgs`
- `sensor_msgs`

### Resultado:

```
going to create a new package
package name: px4_test_cpp
destination directory: /home/fractos/test_px4-ros_ws/src
package format: 3
version: 0.0.0
description: TODO: Package description
maintainer: ['fractos <fractos@todo.todo>']
licenses: ['TODO: License declaration']
build type: ament_cmake
dependencies: ['rclcpp', 'px4_msgs']
creating folder ./px4_test_cpp
creating ./px4_test_cpp/package.xml
creating source and include folder
creating folder ./px4_test_cpp/src
creating folder ./px4_test_cpp/include/px4_test_cpp
creating ./px4_test_cpp/CMakeLists.txt

[WARNING]: Unknown license 'TODO: License declaration'.  This has been set in the package.xml, but no LICENSE file has been created.
It is recommended to use one of the ament license identitifers:
Apache-2.0
BSL-1.0
BSD-2.0
BSD-2-Clause
BSD-3-Clause
GPL-3.0-only
LGPL-3.0-only
MIT
MIT-0
```

#### Estructura generada

```
px4_test_cpp/
├── CMakeLists.txt
├── package.xml
├── include/
│   └── px4_test_cpp/
└── src/
```

##### `package.xml`

Describe el paquete.

Incluye:

- Nombre.
- Versión.
- Autor.
- Licencia.
- Dependencias.

##### `CMakeLists.txt`

Controla el proceso de compilación.

Define:

- Dependencias.
- Ejecutables.
- Instalación.
- Tests.

```CMake title:"Estuctura CMakeList"
find_package(...)
        ↓
add_executable(...)
        ↓
ament_target_dependencies(...)
        ↓
install(...)
        ↓
if(BUILD_TESTING)
    tests
endif()
        ↓
ament_package()
```

###### Añadir un nodo

Ejemplo:

```
add_executable(offboard_node src/offboard_node.cpp)

ament_target_dependencies(
    offboard_node
    rclcpp
    px4_msgs
)

install(
    TARGETS offboard_node
    DESTINATION lib/${PROJECT_NAME}
)
```
---
## Compilar el paquete
![[WorkSpace#Compilar un único paquete]]

![[WorkSpace#Cargar el entorno]]

---
## Ejecutar un nodo

```sh
ros2 run <NAME_PKG> <NODE_NAME>
```

> [!example] Ejemplo:
> 
> ```sh 
> ros2 run px4_test_cpp offboard_node
> ```
> Ejecuta el pkg offboard_node del ws px4_test_cpp

