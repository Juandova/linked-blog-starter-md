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