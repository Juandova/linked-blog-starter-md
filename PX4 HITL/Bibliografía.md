---
tags:
  - drones/autopilot/PX4
  - HITL
date: 2026-09-17
---
> [!warning]  Ojo
> Hay que tener cuidado con tutoriales antiguos que todavía hablan de Fast RTPS, versiones antiguas de Gazebo o configuraciones de PX4 que han cambiado.


## Bloque 1 — PX4 y la Pixhawk 6C

### 1. PX4 User Guide

[PX4 User Guide — documentación oficial](https://docs.px4.io/main/en/)

Es el punto de entrada general.
Investigar:
- [ ] Firmware.
- [ ] Hardware de vuelo.
- [ ] Configuración de la controladora.
- [ ] Parámetros.
- [ ] Comunicación serie.
- [ ] Simulación.

> [!info] **Qué investigar aquí:** 
> cómo se organiza [[PX4]], qué partes se ejecutan en la controladora y cuáles en el ordenador.

---
### 2. Holybro Pixhawk 6C
[Holybro Pixhawk 6C — documentación oficial](https://docs.holybro.com/autopilot/pixhawk-6c)

Investigar:
- [ ] Procesador y memoria.
- [ ] Puertos TELEM1 y TELEM2.
- [ ] UART asociado a cada puerto.
- [ ] Niveles eléctricos.
- [ ] Alimentación de los periféricos.
- [ ] Conexión USB.
- [ ] Compatibilidad con PX4.

**Especialmente importante:** no debemos asumir que TELEM1 y TELEM2 corresponden a los mismos dispositivos internos que en otra Pixhawk.

---

### 3. PX4: Serial Port Configuration
[PX4 — Serial Port Configuration](https://docs.px4.io/main/en/peripherals/serial_configuration)

Esta será una de las páginas fundamentales para tu proyecto.

Aquí se explica cómo configurar los puertos serie para diferentes funciones:
- [ ] MAVLink.
- [ ] uXRCE-DDS.
- [ ] GPS.
- [ ] Telemetría.
- [ ] Otros periféricos.

La idea es entender que un puerto físico no es automáticamente un puerto MAVLink o XRCE-DDS. **Es una UART que PX4 configura mediante parámetros y módulos.**

---
## Bloque 2 — Simulación y HITL

### 4. PX4 Simulation

[PX4 — Simulation](https://docs.px4.io/main/en/simulation/?utm_source=chatgpt.com)

Diferencia entre:
- [ ] [[SITL]].
- [ ] [[HITL]].
- [ ] Simulación con [[Gazebo]].
- [ ] Simulación con otros simuladores.

> [!question] ¿Cómo se conecta un [[PX4]] que se ejecuta en una [[Pixhawk 6C]] física con un simulador Gazebo que se ejecuta en el portátil?
> No debemos dar por hecho que la respuesta sea la misma que para PX4 SITL.

---
### 5. PX4 HITL Simulation

[PX4 — Hardware-in-the-Loop Simulation](https://docs.px4.io/main/en/simulation/hitl?utm_source=chatgpt.com)

> [!important] Investigar esta página antes de configurar nada en la Pixhawk.

Queremos encontrar:

- [ ] Qué firmware utiliza la Pixhawk en HITL.
- [ ] Qué parámetros hay que modificar.
- [ ] Qué simuladores son compatibles.
- [ ] Cómo se conecta la controladora al PC.
- [ ] Qué datos se intercambian entre simulador y Pixhawk.
- [ ] Qué limitaciones tiene HITL respecto a un vuelo real.

---
### 6. Hardware Simulation: SITL, HITL y SIH

[PX4 — Hardware Simulation](https://docs.px4.io/main/en/simulation/hardware?utm_source=chatgpt.com)

PX4 distingue dos formas de simulación sobre hardware real:

| Modalidad          | Dónde se ejecuta la física | Dónde se ejecuta PX4 |
| ------------------ | -------------------------- | -------------------- |
| [[SITL]]           | PC                         | PC                   |
| [[HITL]]           | PC, simulador externo      | Pixhawk              |
| SIH sobre hardware | Pixhawk                    | Pixhawk              |

PX4 documenta que **HITL utiliza un simulador externo como Gazebo Classic o jMAVSim**, mientras que SIH ejecuta un modelo físico directamente en la controladora.

Esto nos da una primera decisión técnica:

> Si quieres que Gazebo sea el motor físico y la Pixhawk ejecute PX4 real, la línea de investigación es HITL.

Pero hay que comprobar la compatibilidad con la versión de Gazebo que utilicemos.

---

## Bloque 3 — ROS 2 y micro XRCE-DDS

### 7. PX4 ROS 2 User Guide

[PX4 — ROS 2 User Guide](https://docs.px4.io/main/en/ros2/user_guide?utm_source=chatgpt.com)

Esta será la referencia principal para la integración ROS 2.

Investiga:

- Arquitectura PX4 ↔ ROS 2.
- uORB.
- uXRCE-DDS.
- Micro XRCE-DDS Client.
- Micro XRCE-DDS Agent.
- `px4_msgs`.
- Publicación de tópicos.
- Suscripción a tópicos.
- Envío de comandos desde ROS 2.

La arquitectura oficial utiliza un **cliente XRCE-DDS en PX4** y un **agente XRCE-DDS en el ordenador o companion computer**. La comunicación puede hacerse mediante serie, UDP, TCP u otros enlaces compatibles.

Esta página es especialmente relevante para tu futuro sistema de enjambres.

---

### 8. uXRCE-DDS: PX4 ↔ ROS 2

[uXRCE-DDS — PX4 Guide](https://docs.px4.io/main/en/middleware/uxrce_dds?utm_source=chatgpt.com)

Aquí está la información que necesitamos para configurar la Pixhawk.

Investiga estos apartados:

1. Architecture.
2. Version selection.
3. PX4 Firmware.
4. Starting the Client.
5. Serial connections.
6. Supported uORB Messages.
7. Customizing the Namespace.

Hay un detalle importante para ti:

**El cliente uXRCE-DDS no sustituye necesariamente al firmware PX4 ni convierte la Pixhawk en un dispositivo ROS 2.** Es un módulo de comunicación que expone determinados mensajes uORB a ROS 2.

El flujo es:

```
PX4
 │
 │ uORB
 ▼
uXRCE-DDS Client
 │
 │ Serial / UDP / TCP
 ▼
Micro XRCE-DDS Agent
 │
 │ DDS
 ▼
ROS 2
```

La documentación también indica que el cliente se incluye en la mayoría de los firmwares, pero hay que comprobarlo en el firmware concreto de la placa.

---

### 9. PX4 + Companion Computer + ROS 2

[PX4 — Raspberry Pi Companion Computer](https://docs.px4.io/main/en/companion_computer/pixhawk_rpi?utm_source=chatgpt.com)

Aunque tú vas a utilizar el portátil y no una Raspberry Pi, **esta guía es probablemente la más útil para tu primera configuración física**.

¿Por qué?

Porque documenta exactamente el tipo de configuración que quieres investigar:

```
Pixhawk
    │
    │ TELEM2
    ▼
uXRCE-DDS
    │
    ▼
Companion Computer
    │
    ▼
Micro XRCE-DDS Agent
    │
    ▼
ROS 2
```

La guía explica cómo:

- Desactivar MAVLink en TELEM2.
- Configurar `UXRCE_DDS_CFG`.
- Configurar la velocidad serie.
- Comprobar el módulo `uxrce_dds_client`.
- Iniciar el Micro XRCE-DDS Agent.
- Ver los tópicos ROS 2.

Para la Pixhawk 6C, la documentación oficial muestra el mapeo:

```
TELEM2 → /dev/ttyS3
```

Y un ejemplo de configuración:

```
MAV_1_CONFIG = 0
UXRCE_DDS_CFG = 102
SER_TEL2_BAUD = 921600
```

Estos parámetros aparecen en la guía de PX4 para conectar ROS 2 a través de TELEM2. **No los apliques todavía:** primero tenemos que confirmar la versión de PX4 y la arquitectura HITL.

---

## Bloque 4 — Radios SiK y telemetría

Aquí hay una cuestión que debemos investigar con cuidado: **una radio SiK no es, por sí misma, una radio XRCE-DDS.**

Normalmente, una radio SiK proporciona un enlace serie transparente. Lo que circula por ese enlace depende de lo que configuremos en los extremos.

Por ejemplo:

```
Pixhawk
    │
    │ TELEM1
    ▼
Radio SiK 915 MHz
    │
    │ Enlace radio
    ▼
Radio SiK USB
    │
    ▼
PC
    │
    ▼
Micro XRCE-DDS Agent
    │
    ▼
ROS 2
```

La investigación consiste en comprobar si podemos transportar XRCE-DDS por ese enlace serie y qué limitaciones introduce.

### 10. PX4 — MAVLink Peripherals

[MAVLink Peripherals — PX4 Guide](https://docs.px4.io/main/en/peripherals/mavlink_peripherals)

Esta página te interesa para comprender cómo PX4 configura sus puertos de telemetría.

Investiga:

- Qué es MAVLink.
- Cómo se configura TELEM1.
- Cómo se configura TELEM2.
- Qué parámetros controlan MAVLink.
- Cómo desactivar MAVLink en un puerto.
- Qué ocurre cuando otro módulo necesita esa UART.

Es importante porque tu objetivo es utilizar un puerto que habitualmente se emplea para MAVLink.

### 11. PX4 — Telemetry Radios

PX4 — Telemetry Radios

Esta es la página que debes utilizar para estudiar la conexión de las radios SiK.

Investiga:

- Conexión física.
- Configuración de telemetría.
- Comunicación con QGroundControl.
- Limitaciones de las radios.
- Velocidades de transmisión.
- Configuración de puertos.

No asumiría todavía que una radio SiK de 915 MHz y 100 mW va a funcionar bien como enlace XRCE-DDS. Hay que validar el comportamiento real.