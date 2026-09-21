---
tags:
  - drones/autopilot/PX4
date: 2026-09-21
---
```NuttShell
uxrce_dds_client status
```

#completar 

### Configuración PX-uXRCE-Radio SiK-ROS

> [!warning]  **[[uXRCE-DDS]] genera un patrón de tráfico mucho más exigente que la telemetría [[MAVLink]] tradicional**.

Mirar otro enlace?? :: [Microhard Telemetry Radio](https://holybro.com/collections/video-data-rc-transmission-system/products/microhard-radio)

[[Configurar baudios SiK Telemetry Radio]]

##### Por qué  probar 115200

Con la configuración anterior:
```
Pixhawk TELEM2 = 57600
SiK Air        = 57600
SiK Ground     = 57600
Agent          = 57600
```

el enlace XRCE consiguió establecer correctamente:

```
create_client
session established
participant created
```

Por tanto, la cadena:

```
Pixhawk → UART → SiK → RF → SiK → USB → MicroXRCEAgent
```

funciona.

Sin embargo, PX4 informa:

```
WARN [timesync] RTT too high for timesync: 222 ms
```

y el cliente permanece:

```text
Running, disconnected
timesync converged: false
cycle: 0 events
```

Además, el MicroXRCEAgent no llega a mostrar operaciones como:

```text
create_topic
create_publisher
create_datawriter
```

Por tanto, la siguiente prueba consiste en aumentar la velocidad serie de las SiK a su máximo documentado:

```text
115200 baud
```

La SiK V3 especifica 115.2 kbps como velocidad máxima de interfaz serie.
