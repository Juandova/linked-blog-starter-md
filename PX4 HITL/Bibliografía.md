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

[PX4 — Simulation](https://docs.px4.io/main/en/simulation/)

- [ ] [[SITL]].
- [ ] [[HITL]].
- [ ] Simulación con [[Gazebo]].
- [ ] Simulación con otros simuladores.

> [!question] ¿Cómo se conecta un [[PX4]] que se ejecuta en una [[Pixhawk 6C]] física con un simulador Gazebo que se ejecuta en el portátil?
> No debemos dar por hecho que la respuesta sea la misma que para PX4 SITL.

---
### 5. PX4 HITL Simulation

[PX4 — Hardware-in-the-Loop Simulation](https://docs.px4.io/main/en/simulation/hitl)

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

[PX4 — Hardware Simulation](https://docs.px4.io/main/en/simulation/hardware)

PX4 distingue dos formas de simulación sobre hardware real:

| Modalidad          | Dónde se ejecuta la física | Dónde se ejecuta PX4 |
| ------------------ | -------------------------- | -------------------- |
| [[SITL]]           | PC                         | PC                   |
| [[HITL]]           | PC, simulador externo      | Pixhawk              |
| SIH sobre hardware | Pixhawk                    | Pixhawk              |

PX4 documenta que **HITL utiliza un simulador externo como Gazebo Classic o jMAVSim**, mientras que SIH ejecuta un modelo físico directamente en la controladora.

> [!info] Si  se quiere que Gazebo sea el motor físico y la Pixhawk ejecute PX4 real, la línea de investigación es HITL.

> [!attention] Pero hay que comprobar la compatibilidad con la versión de Gazebo que utilicemos.

---
## Bloque 3 — ROS 2 y micro XRCE-DDS

### 7. PX4 ROS 2 User Guide

[PX4 — ROS 2 User Guide](https://docs.px4.io/main/en/ros2/user_guide)

Esta será la referencia principal para la integración [[ROS 2]].

Investiga:

- [x] Arquitectura PX4 ↔ ROS 2.
- [ ] [[uORB]].
- [ ] [[uXRCE-DDS]].
- [ ] [[Micro XRCE-DDS Client]].
- [ ] [[Micro XRCE-DDS Agent]].
- [x] [[px4_msgs]].
- [x] Envío de comandos desde ROS 2.

> [!info] La arquitectura oficial utiliza un **cliente XRCE-DDS en PX4** y un [[agente XRCE-DDS]] en el ordenador o companion computer. La comunicación puede hacerse mediante serie, UDP, TCP u otros enlaces compatibles.

---
### 8. uXRCE-DDS: PX4 ↔ ROS 2

[uXRCE-DDS — PX4 Guide](https://docs.px4.io/main/en/middleware/uxrce_dds)


Investiga estos apartados:
1. [ ] Architecture.
2. [ ] Version selection.
3. [ ] PX4 Firmware.
4. [ ] Starting the Client.
5. [ ] Serial connections.
6. [ ] Supported [[uORB Messages]].
7. [ ] Customizing the Namespace.

> [!attention] **El [[cliente uXRCE-DDS]] no sustituye necesariamente al [[firmware PX4]] ni convierte la [[Pixhawk]] en un dispositivo [[ROS 2]].** 
> Es un módulo de comunicación que expone determinados mensajes [[uORB]] a [[ROS 2]].

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

> [!warning]  El cliente se incluye en la mayoría de los firmwares, pero hay que comprobarlo en el firmware concreto de la placa.

---
### 9. PX4 + Companion Computer + ROS 2

[PX4 — Raspberry Pi Companion Computer](https://docs.px4.io/main/en/companion_computer/pixhawk_rpi)

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

Esta guía explica cómo:
- Desactivar MAVLink en TELEM2.
- Configurar `UXRCE_DDS_CFG`.
- Configurar la velocidad serie.
- Comprobar el módulo `uxrce_dds_client`.
- Iniciar el Micro XRCE-DDS Agent.
- Ver los tópicos ROS 2.

Para la [[Pixhawk 6C]], la documentación oficial muestra el mapeo:

```
TELEM2 → /dev/ttyS3
```

Y un ejemplo de configuración:

```
MAV_1_CONFIG = 0
UXRCE_DDS_CFG = 102
SER_TEL2_BAUD = 921600
```

> [!info] Estos parámetros aparecen en la guía de [[PX4]] para conectar [[ROS 2]] a través de TELEM2. 

---
## Bloque 4 — Radios SiK y telemetría

> [!summary] La investigación de este bloque consiste en comprobar si podemos transportar [[XRCE-DDS ]]por ese enlace  y qué limitaciones introduce.

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

> [!info] Holybro Modulo Telemetría SiK V3 915Mhz 100mW 

### 10. PX4 — MAVLink Peripherals

[MAVLink Peripherals — PX4 Guide](https://docs.px4.io/main/en/peripherals/mavlink_peripherals)

Investigar:
- [ ] Qué es MAVLink.
- [ ] Cómo se configura TELEM1.
- [ ] Cómo se configura TELEM2.
- [ ] Qué parámetros controlan MAVLink.
- [ ] Cómo desactivar MAVLink en un puerto.
- [ ] Qué ocurre cuando otro módulo necesita esa UART.

> [!important] Es importante por utilizar un puerto que habitualmente se emplea para MAVLink.

### 11. Holybro SiK Telemetry Radio V3 — Pixhawk 6C + XRCE-DDS

**Objetivo:** investigar cómo utilizar la radio Holybro SiK Telemetry Radio V3 915 MHz 100 mW como enlace de comunicación entre la Pixhawk 6C y el portátil, transportando los datos de micro XRCE-DDS para integrarlos en ROS 2.

#### Hardware

- Controladora: Holybro Pixhawk 6C.
- Radio embarcada: Holybro SiK Telemetry Radio V3 915 MHz 100 mW.
- Radio terrestre: segunda unidad SiK conectada al portátil mediante USB.
- Puerto de conexión previsto: TELEM1 o TELEM2.

#### Documentación oficial

##### 1. Holybro SiK Telemetry Radio V3

[Holybro — SiK Telemetry Radio V3](https://holybro.com/products/sik-telemetry-radio-v3)
	Página oficial del fabricante.

Investigar:

- [ ] Especificaciones de la radio.
- [ ] Conexión a Pixhawk.
- [ ] Conexión USB al PC.
- [ ] Firmware SiK.
- [ ] Configuración de parámetros.
- [ ] Manual de usuario.

 ##### 2. PX4 — Holybro Telemetry Radio

[PX4 — Holybro Telemetry Radio](https://docs.px4.io/main/en/telemetry/holybro_sik_radio)
	Documentación oficial de [[PX4]] para las radios [[Holybro SiK]].

Investigar:
- [ ] Compatibilidad con controladoras Pixhawk.
- [ ] Conexión mediante TELEM1.
- [ ] Uso alternativo de TELEM2.
- [ ] Conexión de la radio terrestre al PC.
- [ ] Configuración y firmware.

##### 3. PX4 — SiK Radio

[PX4 — SiK Radio](https://docs.px4.io/main/en/telemetry/sik_radio)
	Documentación general sobre radios SiK compatibles con PX4.

Investigar:
- [ ] Arquitectura de comunicación.
- [ ] Configuración de los puertos serie.
- [ ] Firmware.
- [ ] Compatibilidad con PX4.
- [ ] Limitaciones del enlace.

---
# Documentación complementaria
### QGroundControl

[QGroundControl User Guide](https://docs.qgroundcontrol.com/)

- [ ] Conectar la Pixhawk.
- [ ] Cargar firmware.
- [ ] Modificar parámetros.
- [ ] Consultar el estado del sistema.
- [ ] Abrir la consola MAVLink.
- [ ] Configurar el vehículo.

### Micro XRCE-DDS Agent

[Micro XRCE-DDS Agent — GitHub](https://github.com/eProsima/Micro-XRCE-DDS-Agent)

- [ ] Instalación.
- [ ] Compilación.
- [ ] Transporte serie.
- [ ] Transporte UDP.
- [ ] Configuración del agente.
- [ ] Compatibilidad con la versión de PX4 y ROS 2.

### PX4 `px4_msgs`

[PX4 — px4_msgs](https://github.com/PX4/px4_msgs)

Es el paquete de mensajes ROS 2 para los nodos C++.

> [!warning] Tendremos que asegurarnos de que las versiones de `px4_msgs` y PX4 sean compatibles.


---
# Normativa 

> [!attention]  la normativa europea establece el marco de uso del espectro radioeléctrico, pero las condiciones concretas de uso en España se determinan mediante el [[CNAF]] y los interfaces radioeléctricos españoles.

> [!summary]  Resumen
> - **433MHz:** la banda que normalmente se utiliza en Europa para determinados dispositivos de corto alcance.
> - **915 MHz:** utilización no puede darse por autorizada simplemente porque el dispositivo se venda en España.

## Europea

### Decisión de Ejecución (UE) 2022/173 de la Comisión

DECISIÓN DE EJECUCIÓN (UE) 2022/173 DE LA COMISIÓN de 7 de febrero de 2022

- [EUR-lex](https://eur-lex.europa.eu/eli/dec_impl/2022/173/oj/eng)
	- [PDF](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32022D0173)

### Decisión de Ejecución (UE) 2019/1345

Decisión de Ejecución (UE) 2019/1345 de la Comisión, de 2 de agosto de 2019.

- [EUR-lex](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32019D1345)
	- [PDF](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32019D1345)

### Decisión de Ejecución (UE) 2018/1538

Decisión de Ejecución (UE) 2018/1538 de la Comisión, de 11 de octubre de 2018.

- [EUR-lex](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32018D1538)
	- [PDF](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX:32018D1538)

## Nacional

### Resolución de 16 de marzo de 2021
Es la **Resolución de 16 de marzo de 2021**, publicada en el BOE como **BOE-A-2021-9918**.

Enlace oficial:
- [BOE — Resolución de 16 de marzo de 2021, interfaces IR-271 a IR-282](https://www.boe.es/buscar/doc.php?id=BOE-A-2021-9918)
	- [PDF que has encontrado](https://digital.gob.es/content/dam/portal-mtdfp/avance-digital/telecomunicacion-e-infraestructuras-digitales/areas_interes/espectro-radioelectrico/informacion-general/interfaces-radielectricos/dispositivos-corto-alcance-srd/Resolucion-271-282.pdf)


### [[CNAF]] 2026

**Orden TDF/732/2026, de 10 de julio, por la que se aprueba el Cuadro Nacional de Atribución de Frecuencias.**

- [BOE — Texto oficial](https://www.boe.es/eli/es/o/2026/07/10/tdf732)
	- [BOE — PDF](https://www.boe.es/eli/es/o/2026/07/10/tdf732/dof/spa/pdf)

Fecha de publicación: 17/07/2026.
Entrada en vigor: 18/07/2026.

> página 23: 5.150: 902-928 MHz en la Región 2 (frecuencia central 915 MHz), están designadas para aplicaciones industriales, científicas y médicas (ICM). Los servicios de radiocomunicación que funcionan en estas bandas deben aceptar la interferencia perjudicial resultante de estas aplicaciones. Los equipos ICM que funcionen en estas bandas estarán sujetos a las disposiciones del número 15.13.

> 5.314A La banda de frecuencias 698-960 MHz, o partes de la misma, en Australia,
Corea, Maldivas, Micronesia, Papúa Nueva Guinea, Tonga y Vanuatu, la banda de
frecuencias 703-733 MHz, 758-788 MHz, 890-915 MHz y 935-960 MHz, o partes de la
misma, en China, India, Indonesia, Japón, Corea (Rep. de), Malasia, Filipinas y Tailandia
se ha identificado para su utilización por estaciones en plataforma a gran altitud como
estaciones base de las Telecomunicaciones Móviles Internacionales (IMT) (HIBS). Esta
identificación no impide el uso de estas bandas de frecuencias por cualquier aplicación
de los servicios a los que están atribuidas ni establece prioridad alguna en el
Reglamento de Radiocomunicacione

> **UN-41 Bandas 880-915 MHz y 925-960 MHz.**
Las bandas de frecuencias 880-915 MHz y 925-960 MHz se reservan para sistemas terrenales capaces de prestar servicios de comunicaciones electrónicas, de conformidad con la [Decisión de Ejecución (UE) 2022/173 de la Comisión](https://eur-lex.europa.eu/eli/dec_impl/2022/173/oj/eng), relativa a la armonización de las bandas de frecuencias de 900 MHz y 1800 MHz para los sistemas terrenales capaces de prestar servicios de comunicaciones electrónicas en la Unión

- **UN-40**


## ETSI EN 300 220

https://www.etsi.org/technical-groups/erm/ 