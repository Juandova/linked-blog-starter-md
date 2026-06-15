---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre/simulación
date: 2026-06-12
---
> [!summary]  
> **Gazebo** es un simulador robótico _open-source_ que permite recrear entornos físicos realistas para probar algoritmos de percepción, control y navegación sin necesidad de utilizar hardware real. Integra motores de física, renderizado 3D y modelos de sensores, siendo ampliamente utilizado junto con [[ROS 2]] y [[PX4]] para validar sistemas autónomos.

> [!hint] Simulación física de robots y vehículos

### ¿Para qué sirve?

Gazebo permite:
- Simular robots y vehículos en entornos tridimensionales.
- Evaluar algoritmos antes de desplegarlos en hardware real.
- Reproducir escenarios complejos de forma segura y repetible.
- Integrar sensores virtuales con modelos físicos.
- Realizar pruebas automatizadas dentro de flujos de integración continua.


> [!info] En el ecosistema [[PX4]], Gazebo actúa como el entorno físico simulado. Mientras que [[PX4]] ejecuta el piloto automático virtual. 
> Gazebo simula:
> - La dinámica del vehículo.
> -  Los sensores.
> - El entorno.
> - La interacción física con el mundo.
> 
>De este modo, ambos sistemas intercambian información para recrear el comportamiento de un vehículo real.

### Características principales

- Motor de física configurable.
- Soporte para múltiples sensores virtuales    
- Arquitectura basada en plugins.
- Integración con [[ROS 2]].
- Integración con [[PX4]] mediante simulaciones [[SITL]].

### Sensores soportados

- Cámaras RGB
- Cámaras de profundidad
- [[IMU]]
- [[GNSS]]
- [[LiDAR]]
- Magnetómetros
- Barómetros
- Sensores personalizados mediante plugins


