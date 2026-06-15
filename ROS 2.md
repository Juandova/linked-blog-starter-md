---
tags:
  - drones/enjambre/ROS
  - MASTER/MUSANTTA/Practicas
date: 2026-06-12
---
> [!summary]  Robot Operating System 2
> **ROS 2** es un _middleware_ de robótica _open-source_ que proporciona un conjunto de bibliotecas, herramientas y convenciones para desarrollar aplicaciones robóticas distribuidas. 
> Facilita la comunicación entre componentes software mediante una arquitectura basada en nodos, permitiendo construir **sistemas complejos de forma modular, escalable y reutilizable**.

> [!hint] Middleware distribuido orientado a sistemas robóticos

### Documentación

- [ROS 2 Documentation](https://docs.ros.org/en/)
- [ROS 2 Humble](https://docs.ros.org/en/humble/)
	- Ubuntu 22.04 LTS
    
- [ROS 2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)
    
- [ROS 2 Concepts](https://docs.ros.org/en/rolling/Concepts.html)
    
- [ROS Index](https://index.ros.org/)
    
- [ROS 2 GitHub](https://github.com/ros2)
    
- [micro-ROS](https://micro.vulcanexus.org/)
	- [[Micro XRCE-DDS]]
    
- [ROS Distributions](https://docs.ros.org/en/rolling/Releases.html)

### "_Instalación_" y creación de un [[WorkSpace]]

```sh
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

```sh
colcon build
```

```sh
source install/setup.bash
```

> [!success]  
> Un _workspace_ de ROS 2 permite agrupar y compilar múltiples paquetes de forma conjunta mediante `colcon`, aislando el desarrollo del resto del sistema.

### Conceptos fundamentales

#### Nodos

Los **nodos** son procesos independientes que implementan funcionalidades concretas dentro del sistema robótico.

Ejemplos:

- Control de motores.
    
- Procesamiento de imágenes.
    
- Localización.
    
- Planificación.
    
- Interfaces de usuario.
    

#### Topics

Los **topics** implementan una comunicación asíncrona basada en publicación/suscripción.

- Un nodo publica mensajes.
- Uno o varios nodos se suscriben.
- No existe acoplamiento directo entre ellos.

#### Services

Los **services** proporcionan comunicación síncrona de tipo petición–respuesta.

Se utilizan cuando:

- Se requiere una respuesta inmediata.
    
- La interacción es puntual.

#### Actions

Las **actions** permiten ejecutar tareas de larga duración con:

- Feedback intermedio.
    
- Cancelación.
    
- Resultado final.
    

#### Parámetros

Los **parámetros** almacenan configuraciones asociadas a cada nodo.

Permiten modificar el comportamiento del sistema sin recompilar.

### Herramientas principales

- `rclcpp`: API cliente para C++.
    
- `rclpy`: API cliente para Python.
    
- `colcon`: sistema de compilación.
    
- `rviz2`: visualización de datos y estados del robot.
    
- `ros2 bag`: grabación y reproducción de mensajes.
    
- `tf2`: gestión de transformaciones entre sistemas de referencia.
    
- `launch`: lanzamiento coordinado de múltiples nodos.
    

### Ventajas

- Arquitectura modular.
    
- Sistemas distribuidos.
    
- Escalabilidad.
    
- Reutilización de componentes.
    
- Compatibilidad con múltiples lenguajes.
    
- Integración con simuladores y hardware real.
    
- Soporte para tiempo real y calidad de servicio (_QoS_).
    

### Compatibilidades

- [[DDS]]: middleware subyacente utilizado para la comunicación entre nodos.
    
- [[Gazebo]]: simulación de robots y entornos.
    
- [[PX4]]: integración para aplicaciones robóticas y vehículos autónomos.
    
- [[micro-ROS]]: extensión de ROS 2 para microcontroladores.
    
- [[RViz2]]: visualización e inspección del estado del sistema.
    
- [[MoveIt]]: planificación de movimiento para manipuladores robóticos.
    
- [[Nav2]]: navegación autónoma para robots móviles.
    

### Casos de uso

- Robots móviles autónomos.
    
- Brazos manipuladores.
    
- Vehículos aéreos no tripulados.
    
- Sistemas multirobot.
    
- Investigación en robótica.
    
- Automatización industrial.
    
- Prototipado rápido de aplicaciones robóticas.
    

