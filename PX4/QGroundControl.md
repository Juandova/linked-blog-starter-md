---
tags:
  - MASTER/MUSANTTA/Practicas
  - drones/autopilot/PX4
date: 2026-06-12
---


> [!summary]  QGroundControl
> **QGC** es una estación de control en tierra (_Ground Control Station_) _open-source_ utilizada para configurar, monitorizar y operar vehículos compatibles con [[PX4]] y el protocolo [[MAVLink]]. Proporciona una interfaz gráfica para gestionar el vehículo sin necesidad de interactuar directamente con el firmware.

> [!hint] Interfaz de usuario para interactuar con el piloto automático

### Documentación

- [QGroundControl](https://qgroundcontrol.com/)
    
- [QGroundControl User Guide](https://docs.qgroundcontrol.com/master/en/)
    
- [QGroundControl Github](https://github.com/mavlink/qgroundcontrol)
    
- [MAVLink](https://mavlink.io/en/)
    

### ¿Para qué sirve?

QGroundControl permite:

- Configurar el piloto automático.
    
- Calibrar sensores.
    
- Planificar misiones.
    
- Monitorizar el estado del vehículo.
    
- Visualizar telemetría en tiempo real.
    
- Registrar y analizar vuelos.
    
- Actualizar el firmware.
    

### Funcionalidades principales

#### Configuración inicial

Permite realizar la puesta en marcha del vehículo:

- Selección del tipo de vehículo.
    
- Configuración de parámetros.
    
- Asignación de modos de vuelo.
    
- Verificación de componentes.
    

#### Calibración

Incluye asistentes para calibrar:

- Acelerómetros.
    
- Giroscopios.
    
- Magnetómetros.
    
- Radio control.
    
- Sensores de nivel.
    

#### Planificación de misiones

Mediante una interfaz gráfica es posible definir:

- Waypoints.
    
- Despegues automáticos.
    
- Aterrizajes.
    
- Órbitas.
    
- Geocercas (_Geofences_).
    
- Acciones asociadas a puntos de ruta.
    

### Monitorización

Durante la operación del vehículo pueden visualizarse:

- Posición GPS.
    
- Altitud.
    
- Estado de batería.
    
- Modos de vuelo.
    
- Estado de sensores.
    
- Mensajes del sistema.
    
- Indicadores de salud.
    

### Registro y análisis

QGroundControl puede almacenar registros (_logs_) para:

- Diagnóstico de fallos.
    
- Ajuste de controladores.
    
- Análisis post-vuelo.
    
- Evaluación del comportamiento del sistema.
    

### Arquitectura de comunicación

QGroundControl se comunica con el vehículo mediante **MAVLink**.

```
QGroundControl
        ↓
     MAVLink
        ↓
PX4 / ArduPilot
        ↓
Vehículo
```

### QGroundControl en simulación

En simulaciones [[SITL]], QGroundControl puede conectarse exactamente igual que lo haría con un vehículo real.

Esto permite:

- Configurar [[PX4]].
    
- Monitorizar la simulación.
    
- Probar misiones.
    
- Validar flujos operativos completos.
    

> [!example]  Ejecutando:
> 
> ```sh
> make px4_sitl gz_x500
> ```
> 
> [[PX4]] inicia un vehículo virtual en [[Gazebo]], al que QGroundControl puede conectarse automáticamente mediante [[MAVLink]].

### Características

- Interfaz gráfica intuitiva.
    
- Compatible con múltiples plataformas.
    
- Amplio soporte para PX4.
    
- Herramientas integradas de configuración.
    
- Planificación visual de misiones.
    
- Útil tanto en simulación como en operación real.
    

### Compatibilidades

- [[PX4]]
    
- ArduPilot
    
- [[MAVLink]]
    
- [[Gazebo]]
    
- [[SITL]]
    
- [[HITL]]
    

## Casos de uso

- Configuración inicial del vehículo.
    
- Operación de drones.
    
- Ensayos en simulación.
    
- Diagnóstico de incidencias.
    
- Ajuste y validación de parámetros.
    
- Formación de pilotos y desarrolladores.
