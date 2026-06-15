---
tags:
  - drones/enjambre/ROS
---


### Intalación

```shell
sudo snap install micro-ros-agent
```


### Launch

```shell
micro-ros-agent udp4 --port 8888
```

Pero la memoria compartida que podemos utilizar es limitada. La podemos intentar ampliar de esta manera:

```shell
micro-ros-agent udp4 --port 8888 --transport-buffer-size 16384
```

desactivarla

```shell
export RMW_FASTRTPS_USE_SHM=0
```

### Paquetes necesarios

```shell
sudo apt install cmake g++ libasio-dev libtinyxml2-dev git libssl-dev
```

Y FastDDS, ya que ROS 2 (Jazzy, Humble...) utiliza Fast DDS como una de las implementaciones posibles de DDS, pero ROS 2 NO instala el SDK completo de Fast DDS (solo las runtime libraries que necesita).

En cambio, para compilar el micro-ros-agent, sí necesitas las bibliotecas de desarrollo de Fast DDS, que incluyen:

fastddsConfig.cmake

cabeceras .hpp

bibliotecas estáticas/dinámicas (.a, .so)

archivos de CMake para ser detectados como find_package(fastdds)

### Instalar Fast-DDS
![[Fast-DDS#Instalación]]

### Instalar micro-ros-msgs

```sh
sudo apt install ros-humble-micro-ros-msgs
```

Dentro del WorkSpace (crear utiles_px4_ws/src):

```sh
git clone -b humble https://github.com/micro-ROS/micro-ROS-Agent.git
```

> [!caution]  
> Si se utiliza el mismo WS para el paquete FastDDS y para micro-ROS, se recomienda utilizar este flag de colcon cuando compilemos:

```sh
colcon build --packages-ignore fastdds
source install/setup.bash
```

Los mensajes de PX4 aunque están en el WS de PX4-Autopilot no se encuentran en el sistema (aunque deberían haberse instalado junto con las librerías) o no los encuentra ROS, por lo que los instalaremos a través de GitHub:

Dentro del workspace:

```sh
git clone https://github.com/PX4/px4_msgs.git
```
Y compilamos:

Desde la raiz del ws:
```sh title:"Instalar dependencias"
rosdep update  
rosdep install --from-paths src --ignore-src -r -y
```

```sh title:"Compilacion simultánea"
colcon build --symlink-install
```



> [!failure]  
> /usr/local/lib/libfastcdr.so.2.2.7

Lo hemos compilado e instalado en el WS  (utiles_px4_ws) donde se encuentran los paquetes micro-ROS-agent y FastDDS.


