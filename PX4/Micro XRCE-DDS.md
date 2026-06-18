---
tags:
  - drones/enjambre
  - drones/autopilot/PX4
date: 2026-06-04
---
> [!summary]  eXtremely Resource Constrained Environments
> Micro XRCE-DDS es una implementación ligera del estándar [[DDS]] diseñada para microcontroladores y sistemas embebidos con recursos muy limitados de memoria y capacidad de procesamiento. Diseñada para microcontroladores y sistemas embebidos con muy poca RAM y CPU
> Permite que dispositivos que no pueden ejecutar una implementación DDS completa participen en ecosistemas basados en [[DDS]] y [[ROS2]] mediante una arquitectura Cliente–Agente.
> Fue desarrollada por [eProsima](https://micro-xrce-dds.docs.eprosima.com/en/v2.2.1/introduction.html)

---

```shell title:"Comando de inicialización"
MicroXRCEAgent udp4 -p 8888
```

El Agent:
- Recibe mensajes XRCE-DDS del cliente.
- Crea los objetos [[DDS]] reales.
- Publica y suscribe tópicos [[DDS]]/[[ROS 2]].
- Actúa como puente hacia [[Fast DDS]].

```sh title:"Inicio para dron físico"
MicroXRCEAgent serial --dev /dev/ttyUSB0 -b 57600
```

---
## Documentación

**Documentación oficial de Micro XRCE-DDS (eProsima):**

[Micro XRCE-DDS Documentation](https://micro-xrce-dds.docs.eprosima.com/?utm_source=chatgpt.com)

**Introducción y arquitectura:**

[Micro XRCE-DDS Overview](https://micro-xrce-dds.docs.eprosima.com/en/latest/introduction.html?utm_source=chatgpt.com)

**Repositorio oficial del Agent:**

[Micro-XRCE-DDS-Agent GitHub](https://github.com/eProsima/Micro-XRCE-DDS-Agent?utm_source=chatgpt.com)

**Documentación oficial de [[PX4]] sobre uXRCE-DDS:**

[PX4 uXRCE-DDS Bridge](https://docs.px4.io/main/en/middleware/uxrce_dds.html?utm_source=chatgpt.com)

----
## Arquitectura

Micro XRCE-DDS utiliza una arquitectura basada en dos componentes.

### Cliente (_Client_)

Se ejecuta en el sistema embebido.

Sus responsabilidades son:

- Publicar datos.
- Suscribirse a Topics.
- Enviar peticiones al Agent.
- Mantener un consumo mínimo de memoria y CPU.

Puede ejecutarse sobre:

- Microcontroladores.
- RTOS.
- Sistemas embebidos ligeros.

### Agent

Se ejecuta en un ordenador o sistema más potente con acceso a DDS.

Sus responsabilidades son:

- Recibir mensajes XRCE-DDS del cliente.
- Crear los objetos [[DDS]] reales.
- Publicar y suscribirse a Topics DDS.
- Gestionar el descubrimiento DDS.
- Actuar como puente hacia implementaciones DDS como [[Fast DDS]].

```
Micro XRCE Client
        ↓
   XRCE Protocol
        ↓
Micro XRCE Agent
        ↓
     DDS
        ↓
     ROS 2
```

> [!success]  
> El Agent traduce las peticiones ligeras del cliente al ecosistema DDS completo.


---
## Ejecución del Agent

Ejemplo utilizando UDP:

```sh title:"Inicialización"
MicroXRCEAgent udp4 -p 8888
```

Esto inicia un Agent que:

- Escucha conexiones XRCE-DDS por UDP.
- Utiliza el puerto `8888`.
- Expone los datos recibidos al dominio DDS correspondiente.

También soporta otros transportes:

- UDP
- TCP
- Serial
- Pseudoterminal (_PTY_)

---
## Micro XRCE-DDS en PX4

[[PX4]] utiliza una variante denominada **uXRCE-DDS Bridge** para exponer información interna del piloto automático hacia [[ROS2]].

El flujo habitual es:

```
uORB
 ↓
uXRCE-DDS Client (PX4)
 ↓
Micro XRCE Agent
 ↓
Fast DDS
 ↓
ROS 2
```

Gracias a este mecanismo:

- Los Topics internos de [[uORB]] pueden publicarse en ROS 2.
- Nodos ROS 2 pueden enviar comandos a PX4.
- No es necesario ejecutar DDS completo dentro del autopiloto.

---
## Características

- Muy bajo consumo de memoria.
- Bajo uso de CPU.
- Compatible con DDS.
- Integración transparente con ROS 2.
- Soporte para múltiples transportes.
- Adecuado para microcontroladores.

### Limitaciones

- No implementa todas las capacidades de DDS.
- Requiere un Agent externo.
- Introduce un salto adicional en la comunicación.
- Algunas funcionalidades avanzadas dependen del Agent utilizado.

## Micro XRCE-DDS vs DDS

|Característica|Micro XRCE-DDS|[[DDS]]|
|---|---|---|
|Objetivo|Sistemas embebidos|Sistemas distribuidos generales|
|Recursos requeridos|Muy bajos|Moderados–altos|
|Descubrimiento|A través del Agent|Nativo|
|Broker/puente|Agent obligatorio|No|
|Uso típico|Microcontroladores|PCs y sistemas completos|
|Integración ROS 2|Mediante Agent|Directa|
