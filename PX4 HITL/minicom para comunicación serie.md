---
tags:
  - drones/autopilot/PX4
date: 2026-09-21
---

> [!summary] ¿Qué es `minicom`?
> `minicom` es un programa de terminal serie para Linux.
>
> Permite comunicarse directamente con dispositivos conectados mediante UART, USB-UART, `/dev/ttyUSB*`, `/dev/ttyACM*`, etc.
>
> Es especialmente útil para configurar y diagnosticar dispositivos que utilizan una interfaz serie.

---
## Instalación

En Ubuntu:

```sh
sudo apt install minicom
```

---

## Abrir un puerto serie

Ejemplo:

```
minicom -D /dev/ttyUSB0 -b 57600
```

Donde:

```
-D /dev/ttyUSB0    dispositivo serie
-b 57600          velocidad
```

También puede configurarse mediante:

```
minicom -s
```

Desde ahí se pueden seleccionar:

- Serial device
- Baud rate
- Data bits
- Parity
- Stop bits
- Hardware Flow Control
- Software Flow Control

---

## Teclas de control

`minicom` utiliza:

```
Ctrl+A
```

como tecla de comando.

Para salir:

```
Ctrl+A
X
```

y confirmar la salida.

---

## Comprobar quién está utilizando el puerto

Antes de abrir `minicom`:

```sh
sudo lsof /dev/ttyUSB0
```

También:

```sh
fuser -v /dev/ttyUSB0
```

Si aparece:

```
MicroXRCEAgent
```

QGroundControl, `screen` o `minicom`, ese programa está utilizando el puerto.

---

## Importante: un puerto serie no puede compartirse normalmente

> [!warning] Puerto exclusivo  
> No debo tener simultáneamente varios programas accediendo a:

```
/dev/ttyUSB0
```

Por ejemplo:

```
QGroundControl
      +
minicom
```

o:

```
screen
      +
MicroXRCEAgent
```

puede provocar:

```
errno: 16
```

o errores de comunicación.


---
## Uso en el proyecto [[PX4]] + SiK

La arquitectura del enlace es:

```
Pixhawk 6C
    │
    │ TELEM2
    │ UART
    ▼
SiK Air Radio
    │
    │ RF
    ▼
SiK Ground Radio
    │
    │ USB
    ▼
/dev/ttyUSB0
```

`minicom` actúa únicamente sobre el último tramo:

```
SiK Ground Radio
       │
       ▼
/dev/ttyUSB0
       │
       ▼
minicom
```

No permite saber directamente si existe enlace RF entre las dos SiK.

---
## Relación con [[Micro XRCE-DDS Agent]]

Para utilizar el puerto con MicroXRCEAgent:

```sh
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 57600
```

debo cerrar previamente `minicom`.

Comprobar:

```sh
sudo lsof /dev/ttyUSB0
```

> [!success] Flujo recomendado
> ```
> minicom
>   ↓
> cerrar con Ctrl+A X
>   ↓
> comprobar /dev/ttyUSB0
>   ↓
> MicroXRCEAgent
> ```
