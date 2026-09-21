---
tags:
  - drones/autopilot/
---
> [!summary] ¿Qué es `screen`?
> `screen` es un multiplexor de terminal que, además de permitir mantener sesiones de terminal persistentes, puede utilizarse como un terminal serie.
>
> Es útil para conectarse directamente a dispositivos que aparecen como `/dev/ttyUSB*` o `/dev/ttyACM*`.

---
## Uso básico

Para abrir un puerto serie:

```sh
screen /dev/ttyUSB0 57600
```

La sintaxis general es:

```
screen <dispositivo> <baudrate>
```
Por ejemplo:
```
screen /dev/ttyUSB0 115200
```

---
## En el proyecto [[PX4]] + SiK

En mi sistema:
```
SiK Ground Radio
      │
      │ USB
      ▼
/dev/ttyUSB0
      │
      ▼
MicroXRCEAgent
```

Por tanto, `screen` permite abrir directamente el puerto USB de la radio.

> [!warning] El puerto serie solo puede tener un propietario  
> Si `screen` tiene abierto `/dev/ttyUSB0`, otro programa como `MicroXRCEAgent`, `minicom`, QGroundControl o Mission Planner puede recibir:
> ```
> errno: 16
> ```
> 
> porque el dispositivo está ocupado.

Para comprobar quién está utilizando el puerto:

```sh
sudo lsof /dev/ttyUSB0
```

También:

```sh
fuser -v /dev/ttyUSB0
```

---

## Salir de `screen`

Dentro de `screen`:
```
Ctrl+A
K
```
Después confirmar:
```
y
```
También se pueden listar las sesiones:
```sh
screen -ls
```
Y cerrar una sesión concreta:
```
screen -S <ID> -X quit
```
Ejemplo:
```sh
screen -S 12345 -X quit
```
---

## Comprobar si `screen` está ocupando el puerto

```sh
sudo lsof /dev/ttyUSB0
```

Si aparece algo como:

```sh
screen  12345  fractos  ... /dev/ttyUSB0
```

el puerto está siendo utilizado por `screen`.

---

## Relación con [[Micro XRCE-DDS Agent]]

No puedo ejecutar simultáneamente:

```sh
screen /dev/ttyUSB0 57600
```

y:

```sh
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 57600
```

porque ambos intentan abrir el mismo dispositivo.

> [!success] Regla práctica  
> Para depurar manualmente:

```
detener MicroXRCEAgent
      ↓
abrir screen/minicom
      ↓
realizar prueba
      ↓
cerrar screen/minicom
      ↓
iniciar MicroXRCEAgent
```