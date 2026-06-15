---
tags:
  - drones/enjambre
  - drones/autopilot/PX4
date: 2026-06-04
---

> [!summary] px4-uxrce_dds_client
> es un módulo de [[PX4]] que implementa el **cliente Micro XRCE-DDS**. Su función es actuar como puente entre los mensajes internos de PX4 ([[uORB]]) y el ecosistema **[[DDS]]/[[ROS 2]]**. Gracias a este módulo, una computadora compañera (Raspberry Pi, Jetson, NUC, etc.) puede intercambiar datos con el autopiloto PX4 usando ROS 2 de forma nativa.

> [!hint]  Es el traductor entre el mundo interno de PX4 y el mundo DDS/ROS 2.


[uxrce_dds_client](https://docs.px4.io/main/en/modules/modules_system#uxrce-dds-client)


el ejecutable “px4-uxrce_dds_client”, que nos proporciona un cliente [[RTPS]] para la comunicación vía “micro” [[DDS]] (como un protocolo para sistemas embebidos), el [[Micro XRCE-DDS]](Extremaly Resource Constrained Environment).

## Arquitectura

PX4 (uORB)
    │
    ▼
uxrce_dds_client
    │  UDP o Serial
    ▼
Micro XRCE-DDS Agent
    │
    ▼
[[ROS 2]] / DDS Network

### Flujo de datos

#### De PX4 hacia ROS 2

```
vehicle_attitude
      ↓
uORB
      ↓
uxrce_dds_client
      ↓
XRCE-DDS
      ↓
Agent
      ↓
DDS
      ↓
ROS 2 Topic
```

#### De ROS 2 hacia PX4

```
ROS 2 Topic
      ↓
DDS
      ↓
Agent
      ↓
XRCE-DDS
      ↓
uxrce_dds_client
      ↓
uORB
      ↓
PX4
```
### Parámetros importantes en PX4

- `UXRCE_DDS_CFG` → interfaz de comunicación (TELEM2, Ethernet, WiFi, etc.).
- `UXRCE_DDS_AG_IP` → IP del agente DDS.
- `UXRCE_DDS_PRT` → puerto UDP (por defecto 8888).
- `UXRCE_DDS_DOM_ID` → DDS Domain ID.
- `UXRCE_DDS_KEY` → identificador único del cliente.

## Ejecución del Agent

En la computadora compañera debe ejecutarse el Agent correspondiente.

Ejemplo mediante UDP:

```sh
MicroXRCEAgent udp4 -p 8888
```

El Agent:

- Recibe mensajes XRCE-DDS del cliente PX4.
- Crea entidades DDS reales.
- Publica Topics DDS.
- Gestiona suscripciones DDS.
- Actúa como puente hacia [[Fast DDS]].


## Instalación

```sh 
git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git
cd Micro-XRCE-DDS-Agent
mkdir build && cd build
```


```sh
cmake ..
make
sudo make install
```

> [!info]  On Windows first select the Visual Studio version:
```PowerShell
cmake -G "Visual Studio 15 2017 Win64" ..
cmake --build .
cmake --build . --target install
```

## Topics expuestos

No todos los Topics de [[uORB]] se exportan automáticamente.

PX4 utiliza archivos de configuración para definir qué mensajes se sincronizan entre ambos mundos.

Estos archivos especifican:

- Topics publicados hacia ROS 2.
- Topics recibidos desde ROS 2.
- Tipos de mensaje asociados.

## Relación con otros componentes

| Componente         | Función                                    |
| ------------------ | ------------------------------------------ |
| [[uORB]]           | Comunicación interna de PX4                |
| `uxrce_dds_client` | Traducción uORB ↔ XRCE                     |
| [[Micro XRCE-DDS]] | Protocolo ligero cliente–agente            |
| [[DDS]]            | Middleware distribuido                     |
| [[Fast-DDS]]       | Implementación DDS utilizada habitualmente |
| [[ROS 2]]          | Aplicaciones robóticas externas            |

## Documentación

**Guía principal de PX4 (actual):**

[PX4 uXRCE-DDS (PX4-ROS 2/DDS Bridge)](https://docs.px4.io/main/en/middleware/uxrce_dds.html)

[uxrce_dds_client](https://docs.px4.io/main/en/modules/modules_system#uxrce-dds-client)

**Versión PX4 1.14:**

[PX4 v1.14 uXRCE-DDS Guide](https://docs.px4.io/v1.14/en/middleware/uxrce_dds.html)

**Repositorio oficial del agente Micro XRCE-DDS:**

[eProsima Micro XRCE-DDS Agent](https://github.com/eProsima/Micro-XRCE-DDS-Agent)

[Installation Manual](https://micro-xrce-dds.docs.eprosima.com/en/latest/installation.html)