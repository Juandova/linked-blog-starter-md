---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/enjambre
date: 2026-06-10
---
> [!summary]  Ejecuta todos los drones [[PX4]], [[Gazebo]], [[Micro XRCE-DDS]] y [[QGroundControl]]


## Ejecución

```sh title:"Ejecución básica"
ros2 launch swarm_launch swarm_launch.launch.py num_drones:=5 cols:=5 spacing:=2
```

```sh title:"Ejecución con todos los argumentos"
ros2 launch swarm_launch swarm_launch.launch.py num_drones:=5 cols:=3 spacing:=2 home_lat:=39.48053 home_lon:=-0.33928 home_alt:=9 show_drone_terminals:=false
```

para parar todos los procesos: 
```sh
pkill -f px4
pkill -f gz
pkill -f gazebo
pkill -f MicroXRCEAgent
pkill -f QGroundControl
pkill -f gnome-terminal
pkill -f "swarm_pkg drone_node"
```


## Explicación del Código

> [!summary]  `*.launch.py`
> **Se trata de descripciones declarativas que [[ROS 2]] ejecuta mediante un motor de lanzamiento (`launch`)**.

> [!question]  ¿Quién está llamando a estas funciones?
> No las llamas tú. Las llama el motor de `launch` de [[ROS 2 ]]cuando encuentra las acciones correspondientes dentro del `LaunchDescription`.

> [!hint] Es decir, es una lista de tareas para ROS


La cadena de `swarm_launch.launch.py`  es:

```
ros2 launch
    ↓
generate_launch_description()
    ↓
LaunchDescription(...)
    ↓
encuentra OpaqueFunction
    ↓
OpaqueFunction llama a _launch_swarm()
    ↓
_launch_swarm devuelve acciones
    ↓
ROS ejecuta esas acciones
```


> [!tip]  `generate_launch_description()` es el equivalente al `main()` de un archivo `.launch.py`, y `OpaqueFunction` existe porque algunos valores solo se conocen cuando ROS ya está ejecutando el launch.

#### `TimerAction`

> [!info]  Le dice a ROS cuando ejecutar tal acción

```py title:"Ejemplo de TimerAction"
TimerAction(
    period=5.0,
    actions=[
        _terminal(...)
    ]
)
```

#### `_terminal()`

> [!info] Fabrica un objeto del tipo `ExecuteProcess(...)`
> Que significa que, cuando ROS decida, abre este gnome-terminal
 
```py
def _terminal(title, command):
    return ExecuteProcess(...)
```

#completar 


> [!summary]  `os.environ` es un diccionario con las variables de entorno del sistema.

