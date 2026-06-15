---
tags:
  - drones/autopilot/PX4
date: 2026-06-12
---

> [!summary]  
> **uORB** es el sistema interno de comunicación basado en publicación/suscripción utilizado por [[PX4]]. 
> Permite que los distintos módulos del piloto automático intercambien información de forma desacoplada y eficiente, constituyendo el principal mecanismo de paso de mensajes dentro del firmware.

> [!hint] El "bus de mensajes" interno de [[PX4]]

### Documentación

- [uORB Messaging](https://docs.px4.io/main/en/middleware/uorb.html)
- [PX4 Message Definitions](https://github.com/PX4/PX4-Autopilot/tree/main/msg)
    
- [PX4 Architecture](https://docs.px4.io/main/en/concept/architecture.html)
    
- [PX4-Autopilot Github](https://github.com/PX4/PX4-Autopilot)
    

### ¿Por qué existe uORB?

Un piloto automático moderno está formado por numerosos módulos independientes:

- Lectura de sensores.
    
- Estimación del estado.
    
- Control de actitud.
    
- Control de posición.
    
- Navegación.
    
- Gestión de actuadores.
    
- Comunicación externa.
    

Sin un mecanismo de comunicación común, estos módulos estarían fuertemente acoplados entre sí.

uORB resuelve este problema proporcionando una infraestructura interna de mensajería.

### Modelo de comunicación

uORB utiliza un esquema de **publicación/suscripción**.

- Los módulos publican mensajes.
    
- Otros módulos se suscriben a dichos mensajes.
    
- Productores y consumidores permanecen desacoplados.
    

```
IMU
 │
 ▼
sensor_combined
 │
 ├────► Estimador
 │
 ├────► Logger
 │
 └────► Controladores
```

### Conceptos fundamentales

#### Topic

Los **Topics** representan flujos de información concretos.

Ejemplos:

- `sensor_combined`
    
- `vehicle_attitude`
    
- `vehicle_local_position`
    
- `vehicle_status`
    
- `actuator_outputs`
    

Cada Topic posee un tipo de dato asociado.

#### Publisher

Módulo encargado de generar información.

Ejemplos:

- Drivers de sensores.
    
- Estimadores.
    
- Generadores de trayectorias.
    

#### Subscriber

Módulo que consume información publicada.

Ejemplos:

- Controladores.
    
- Registradores de vuelo.
    
- Interfaces externas.
    

### Definición de mensajes

Los mensajes uORB se definen mediante archivos `.msg`.

Ejemplo:

```
float32 roll
float32 pitch
float32 yaw
uint64 timestamp
```

Durante la compilación, [[PX4]] genera automáticamente el código necesario para publicar y suscribirse a estos mensajes.

### Flujo típico dentro de PX4

```
Sensores
   ↓
Drivers
   ↓
uORB
   ↓
Estimadores
   ↓
Controladores
   ↓
uORB
   ↓
Actuadores
```

> [!success]  
> uORB permite que cada módulo de PX4 pueda evolucionar independientemente sin modificar el resto del sistema.

### Ventajas

- Bajo acoplamiento.
    
- Arquitectura modular.
    
- Alta eficiencia.
    
- Comunicación asíncrona.
    
- Facilita el mantenimiento.
    
- Simplifica la incorporación de nuevos módulos.
    

### uORB y DDS

Aunque ambos utilizan publicación/suscripción, cumplen funciones diferentes:

|Característica|uORB|[[DDS]]|
|---|---|---|
|Alcance|Interno a PX4|Sistemas distribuidos|
|Ejecución|Dentro del firmware|Entre procesos o equipos|
|Descubrimiento|Estático|Automático|
|Tiempo real|Muy alto|Alto|
|Uso principal|Comunicación interna|Comunicación externa|

### uORB y [[ROS 2]]

PX4 expone determinados Topics uORB hacia [[ROS 2]] mediante **micro XRCE-DDS**.

```
uORB
 ↓
micro XRCE-DDS
 ↓
DDS
 ↓
ROS 2
```

De esta forma, aplicaciones externas pueden acceder a información del piloto automático.
