---
tags:
  - drones/autopilot/PX4
date: 2026-09-21
---
> [!summary]  
> Las SiK Telemetry Radio V3 admiten varias velocidades de interfaz serie:
> 
> `1200`, `2400`, `4800`, `9600`, `19200`, `38400`, `57600` y `115200` baudios.
> 
> La configuración de fábrica habitual es **57600 baudios**.
> 
> Para la prueba con **[[Micro XRCE-DDS]]**, se quiere aumentar la velocidad de la interfaz serie a **115200 baudios** para reducir la latencia del enlace.
> 
> **Importante:** esto cambia la velocidad UART entre el equipo y la radio. No significa que la radio transmita por RF a 115200 bit/s. La velocidad RF (`AIR_SPEED`) es un parámetro independiente.

---
## 1. Arquitectura de la prueba

Actualmente:
```
Pixhawk 6C
    │
    │ TELEM2
    │ UART
    ▼
┌───────────────┐
│ SiK Air Radio │
└───────┬───────┘
        │
        │ RF
        ▼
┌────────────────┐
│ SiK Ground     │
│ Radio          │
└───────┬────────┘
        │ USB
        ▼
/dev/ttyUSB0
        │
        ▼
MicroXRCEAgent
        │
        ▼
ROS 2
```

La configuración debe ser coherente en los **tres puntos serie**:
```
Pixhawk SER_TEL2_BAUD = 115200
          │
          ▼
      SiK Air UART = 115200
          │
          │ RF
          ▼
     SiK Ground UART = 115200
          │
          ▼
MicroXRCEAgent -b 115200
```


---

# 3. Método recomendado: AT Commands

Las SiK utilizan un conjunto de comandos AT similar al de un módem.

El parámetro que nos interesa es:

```text
S1 = SERIAL_SPEED
```

La documentación de SiK utiliza una representación abreviada para la velocidad:

```text
S1: SERIAL_SPEED=57
```

significa:

```text
57600 baud
```

Por tanto:

```text
S1: SERIAL_SPEED=115
```

significa:

```text
115200 baud
```

---

## 4. Configurar la SiK Ground

Primero conectar la **SiK Ground Radio** al ordenador mediante USB.

Comprobar el puerto:

```bash
ls -l /dev/ttyUSB*
```

En nuestro caso:

```text
/dev/ttyUSB0
```

Antes de abrirlo, asegurarse de que QGroundControl no lo está utilizando.

Comprobar:

```bash
sudo lsof /dev/ttyUSB0
```

Si no aparece ningún proceso, podemos acceder al puerto.

---

## 5. Entrar en modo AT

La radio debe estar conectada al ordenador utilizando **la velocidad serie actual**.

Actualmente:

```text
57600 baud
```

Por ejemplo:

```bash
screen /dev/ttyUSB0 57600
```

Esperar aproximadamente un segundo sin enviar nada.

Después introducir:

```text
+++
```

La radio debería responder:

```text
OK
```

> [!warning]  
> `+++` tiene un tiempo de guarda.
> 
> Hay que dejar aproximadamente **1 segundo sin transmitir antes y después** de la secuencia.
> 
> Si se escribe inmediatamente después de abrir el terminal o mientras existe tráfico, puede no entrar en modo AT.

---

# 6. Comprobar la configuración actual

Una vez aparezca:

```text
OK
```

ejecutar:

```text
ATI5
```

Esto muestra los parámetros configurables.

Debería aparecer algo parecido a:

```text
S0: FORMAT=22
S1: SERIAL_SPEED=57
S2: AIR_SPEED=64
...
```

Lo importante es:

```text
S1: SERIAL_SPEED=57
```

que corresponde a:

```text
57600 baud
```

---

# 7. Cambiar a 115200

Ejecutar:

```text
ATS1=115
```

La radio debería aceptar el cambio.

Después guardar la configuración:

```text
AT&W
```

Y reiniciar:

```text
ATZ
```

La configuración quedará:

```text
S1: SERIAL_SPEED=115
```

equivalente a:

```text
115200 baud
```

---

# 8. ¡Importante! La conexión del terminal dejará de funcionar

Después de ejecutar:

```text
ATS1=115
AT&W
ATZ
```

la radio pasa a trabajar a:

```text
115200 baud
```

Por tanto, el terminal que estaba abierto a:

```text
57600
```

ya no podrá comunicarse correctamente con ella.

Cerrar `screen`:

```text
Ctrl+A
K
y
```

Después volver a abrirlo a:

```bash
screen /dev/ttyUSB0 115200
```

Y volver a entrar en AT:

```text
+++
```

Finalmente comprobar:

```text
ATI5
```

y verificar:

```text
S1: SERIAL_SPEED=115
```

---

# 9. Configurar también la SiK Air

Las dos radios deben utilizar la misma velocidad serie.

La **SiK Air Radio** está conectada al:

```text
Pixhawk 6C TELEM2
```

Por tanto, hay que configurarla también a:

```text
115200
```

La forma más sencilla es desconectarla temporalmente del Pixhawk y conectarla mediante USB al ordenador.

Repetir:

```text
screen /dev/ttyUSB0 57600
```

Entrar en AT:

```text
+++
```

Comprobar:

```text
ATI5
```

Cambiar:

```text
ATS1=115
```

Guardar:

```text
AT&W
```

Reiniciar:

```text
ATZ
```

Después volver a conectar a:

```text
115200
```

y verificar:

```text
ATI5
```

Debe aparecer:

```text
S1: SERIAL_SPEED=115
```

---

# 10. Configurar PX4

En la Pixhawk:

```text
SER_TEL2_BAUD = 115200
```

Desde NSH:

```text
param set SER_TEL2_BAUD 115200
```

Comprobar:

```text
param show SER_TEL2_BAUD
```

Debe mostrar:

```text
SER_TEL2_BAUD: 115200
```

La configuración de uXRCE-DDS continúa siendo:

```text
UXRCE_DDS_CFG = 102
```

porque:

```text
102 = TELEM2
```

---

# 11. Configurar MicroXRCEAgent

En el ordenador:

```bash
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 115200
```

No utilizar:

```bash
-b 57600
```

porque la SiK Ground ahora trabaja a:

```text
115200
```

---

# 12. Secuencia de arranque

Para evitar problemas de diagnóstico, utilizar esta secuencia:

### 1. SiK Ground

Conectar:

```text
SiK Ground → USB → PC
```

Comprobar:

```bash
ls -l /dev/ttyUSB0
```

### 2. MicroXRCEAgent

Arrancar:

```bash
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 115200 -v 6
```

### 3. Pixhawk

Conectar/alimentar la Pixhawk.

Comprobar:

```text
uxrce_dds_client status
```

### 4. Esperar la conexión

En el Agent debería aparecer algo parecido a:

```text
create_client
session established
participant created
```

Y, si la conexión funciona correctamente, esperamos posteriormente operaciones como:

```text
create_topic
create_publisher
create_datawriter
```

En PX4 también esperamos que desaparezca:

```text
RTT too high for timesync
```

y que:

```text
timesync converged: true
```

---

# 13. Comprobación desde ROS 2

Una vez establecida la sesión:

```bash
ros2 node list
```

y:

```bash
ros2 topic list
```

Deberían empezar a aparecer los tópicos de PX4.

Por ejemplo:

```text
/fmu/out/vehicle_status
/fmu/out/vehicle_local_position
...
```

Comprobar:

```bash
ros2 topic list | grep /fmu
```

Y después:

```bash
ros2 topic echo /fmu/out/vehicle_status
```

---

# 14. Qué queremos comprobar exactamente

Esta prueba tiene un objetivo muy concreto.

### Antes

```text
SiK UART       57600
Agent          57600
PX4 TELEM2     57600

RTT ≈ 222 ms

timesync converged: false
cycle: 0
datawriters: NO
```

### Después

```text
SiK UART       115200
Agent          115200
PX4 TELEM2     115200

RTT ↓
```

La hipótesis es que la reducción de latencia permita que PX4 complete la sincronización temporal y continúe con la creación de las entidades DDS.

> [!success]  
> **Criterio de éxito**
> 
> No basta con que aparezca:
> 
> ```text
> session established
> ```
> 
> Eso ya lo conseguimos a 57600.
> 
> El objetivo de esta prueba es llegar a:
> 
> ```text
> timesync converged: true
> ```
> 
> y que el Agent muestre operaciones de creación de:
> 
> ```text
> topics
> publishers
> datawriters
> ```
> 
> Después deberán aparecer los tópicos `/fmu/...` en ROS 2.

---

# 15. Alternativa: Mission Planner

Las SiK también pueden configurarse mediante **Mission Planner**.

La configuración equivalente es:

```text
SERIAL_SPEED = 115
```

o:

```text
115200 baud
```

Mission Planner permite configurar las radios SiK y también actualizar su firmware.

Para esta prueba, sin embargo, los **AT commands** son útiles porque permiten documentar exactamente qué parámetro se ha modificado.

---

# 16. Parámetro importante: SERIAL_SPEED ≠ AIR_SPEED

No confundir:

```text
SERIAL_SPEED
```

con:

```text
AIR_SPEED
```

### SERIAL_SPEED

Velocidad UART entre:

```text
Pixhawk ↔ SiK
```

y:

```text
SiK ↔ USB/PC
```

Valores disponibles en la SiK V3:

```text
1.2
2.4
4.8
9.6
19.2
38.4
57.6
115.2 kbps
```

### AIR_SPEED

Velocidad de transmisión de datos por RF.

Valores disponibles en la SiK V3 incluyen:

```text
2
4
8
16
32
64
96
128
192
250 kbps
```

Por ahora **no modificar `AIR_SPEED`**.

La prueba que queremos hacer consiste únicamente en:

```text
SERIAL_SPEED:
57600 → 115200
```

---

# 17. Estado esperado después de la configuración

```text
                    UART 115200
Pixhawk 6C ───────────────────────── SiK Air
                                      │
                                      │ RF
                                      │
                                   SiK Ground
                                      │
                                      │ USB/UART 115200
                                      ▼
                               /dev/ttyUSB0
                                      │
                                      ▼
                              MicroXRCEAgent
                                      │
                                      ▼
                                    DDS
                                      │
                                      ▼
                                   ROS 2
```

> [!fail]  
> Si después de pasar a 115200 seguimos obteniendo:
> 
> ```text
> RTT too high for timesync
> ```
> 
> y:
> 
> ```text
> timesync converged: false
> ```
> 
> entonces tendremos una evidencia mucho más fuerte de que **el problema no es simplemente el baudrate UART de 57600**.
> 
> En ese caso habría que investigar el comportamiento temporal del enlace SiK/uXRCE-DDS antes de cambiar de arquitectura.

---

## Referencias

- Holybro — SiK Telemetry Radio V3:  
    [https://holybro.com/products/sik-telemetry-radio-v3](https://holybro.com/products/sik-telemetry-radio-v3)
    
- ArduPilot — SiK Radio Advanced Configuration:  
    [https://ardupilot.ardupilot.org/sub/docs/common-3dr-radio-advanced-configuration-and-technical-information.html](https://ardupilot.ardupilot.org/sub/docs/common-3dr-radio-advanced-configuration-and-technical-information.html)
    
- Holybro — Downloads / Quick Start Guide:  
    [https://holybro.com/pages/downloads](https://holybro.com/pages/downloads)