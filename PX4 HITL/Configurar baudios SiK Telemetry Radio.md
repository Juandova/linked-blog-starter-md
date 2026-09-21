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

> [!attention] **Importante:** 
> esto cambia la velocidad UART entre el equipo y la radio. No significa que la radio transmita por RF a 115200 bit/s. La velocidad RF (`AIR_SPEED`) es un parámetro independiente.

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

```
S1 = SERIAL_SPEED
```

La documentación de SiK utiliza una representación abreviada para la velocidad:

```
S1: SERIAL_SPEED=57
```

significa:

```
57600 baud
```

Por tanto:

```
S1: SERIAL_SPEED=115
```

significa:

```
115200 baud
```

---
## 4. Configurar la SiK Ground

Primero conectar la **SiK Ground Radio** al ordenador mediante USB.

Comprobar el puerto:

```sh
ls -l /dev/ttyUSB*
```

> [!example] En nuestro caso:
> ```
>/dev/ttyUSB0
>```

Antes de abrirlo, asegurarse de que [[QGroundControl]] no lo está utilizando.

Comprobar:
```sh
sudo lsof /dev/ttyUSB0
```

Si no aparece ningún proceso, podemos acceder al puerto.

---
## 5. Entrar en modo AT

La radio debe estar conectada al ordenador utilizando **la velocidad serie actual**.

> [!warning]  Importante
> La radio tiene que estar en silencio. Así que hay que apagar la pixhawk.

Actualmente:

```
57600 baud
```

Por ejemplo:
```sh
screen /dev/ttyUSB0 57600
```

Esperar aproximadamente un segundo sin enviar nada.

Después introducir:

```
+++
```

La radio debería responder:

```
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

```
OK
```

ejecutar:

```
ATI5
```

Esto muestra los parámetros configurables.

Debería aparecer algo parecido a:
``` title:"Resultado de ATI5"
ATI5
S0:FORMAT=26
S1:SERIAL_SPEED=57
S2:AIR_SPEED=64
S3:NETID=25
S4:TXPOWER=20
S5:ECC=0
S6:MAVLINK=1
S7:OPPRESEND=0
S8:MIN_FREQ=915000
S9:MAX_FREQ=928000
S10:NUM_CHANNELS=50
S11:DUTY_CYCLE=100
S12:LBT_RSSI=0
S13:MANCHESTER=0
S14:RTSCTS=0
S15:MAX_WINDOW=131
```

Lo importante es:

```
S1: SERIAL_SPEED=57
```

que corresponde a:

```
57600 baud
```

---

# 7. Cambiar a 115200

Ejecutar:

```Screen
ATS1=115
```

La radio debería aceptar el cambio.

Después guardar la configuración:

```screen
AT&W
```

Y reiniciar:

```screen
ATZ
```

La configuración quedará:
```
S1: SERIAL_SPEED=115
```

equivalente a:
```
115200 baud
```

---
# 8. ¡Importante! La conexión del terminal dejará de funcionar

Después de ejecutar:

```
ATS1=115
AT&W
ATZ
```

la radio pasa a trabajar a:

```
115200 baud
```

Por tanto, el terminal que estaba abierto a:

```
57600
```

ya no podrá comunicarse correctamente con ella.

Cerrar `screen`:

```
Ctrl+A
K
y
```

Después volver a abrirlo a:

```
screen /dev/ttyUSB0 115200
```

Y volver a entrar en AT:

```
+++
```

Finalmente comprobar:

```
ATI5
```

y verificar:

```
S1: SERIAL_SPEED=115
```

---
# 9. Configurar también la SiK Air

Las dos radios deben utilizar la misma velocidad serie.

La **SiK Air Radio** está conectada al:

```
Pixhawk 6C TELEM2
```

Por tanto, hay que configurarla también a:

```
115200
```

> [!tip] La forma más sencilla es desconectarla temporalmente del Pixhawk y conectarla mediante USB al ordenador.

Repetir:

```
screen /dev/ttyUSB0 57600
```

Entrar en AT:

```
+++
```

Comprobar:

```
ATI5
```

Cambiar:

```
ATS1=115
```

Guardar:

```
AT&W
```

Reiniciar:

```
ATZ
```

Después volver a conectar a:

```
115200
```

y verificar:

```
ATI5
```

Debe aparecer:

```
S1: SERIAL_SPEED=115
```

---

# 10. Configurar PX4

En la Pixhawk:

```
SER_TEL2_BAUD = 115200
```

Desde NSH:

```
param set SER_TEL2_BAUD 115200
```

Comprobar:

```
param show SER_TEL2_BAUD
```

Debe mostrar:

```
SER_TEL2_BAUD: 115200
```

La configuración de uXRCE-DDS continúa siendo:

```
UXRCE_DDS_CFG = 102
```

porque:

```
102 = TELEM2
```

---

# 11. Configurar MicroXRCEAgent

En el ordenador:

```sh
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 115200
```

No utilizar:

```
-b 57600
```

porque la SiK Ground ahora trabaja a:

```
115200
```

---



---------

# 12. Secuencia de arranque

Para evitar problemas de diagnóstico, utilizar esta secuencia:

### 1. SiK Ground

Conectar:

```
SiK Ground → USB → PC
```

Comprobar:

```sh
ls -l /dev/ttyUSB0
```

### 2. MicroXRCEAgent

Arrancar:

```sh
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 115200 -v 6
```

### 3. Pixhawk

Conectar/alimentar la Pixhawk.

Comprobar:

```nsh
uxrce_dds_client status
```

### 4. Esperar la conexión

En el Agent debería aparecer algo parecido a:

```
create_client
session established
participant created
```

Y, si la conexión funciona correctamente, esperamos posteriormente operaciones como:

```
create_topic
create_publisher
create_datawriter
```

En PX4 también esperamos que desaparezca:

```
RTT too high for timesync
```

y que:

```
timesync converged: true
```

---

# 13. Comprobación desde ROS 2

Una vez establecida la sesión:

```sh
ros2 node list
```

y:

```sh
ros2 topic list
```

Deberían empezar a aparecer los tópicos de [[PX4]].

Por ejemplo:

```
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