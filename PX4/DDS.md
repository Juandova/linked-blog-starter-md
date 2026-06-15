---
tags:
  - drones/enjambre
  - informática/comunicaciones
  - drones/autopilot/PX4
date: 2026-06-04
---
> [!summary]  Data Distribution Service
> **DDS** es un estándar de comunicación orientado a sistemas distribuidos en tiempo real basado en el paradigma de publicación/suscripción (_publish-subscribe_). 
> Permite que diferentes aplicaciones **intercambien datos** de forma eficiente, desacoplada y configurable, sin necesidad de un servidor central.

> [!hint] Middleware de comunicación distribuida para sistemas en tiempo real

### Documentación

- [OMG DDS Specification](https://www.omg.org/spec/DDS/)
    
- [DDS Foundation](https://www.dds-foundation.org/)
    
- [eProsima Fast DDS](https://fast-dds.docs.eprosima.com/)
    
- [Cyclone DDS Documentation](https://cyclonedds.io/docs/)
    
- [ROS 2 Concepts - DDS](https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Different-Middleware-Vendors.html)
    
- [RTI Connext DDS](https://www.rti.com/products/dds-standard)
    

### Modelo de comunicación

DDS utiliza un esquema de **publicación/suscripción**.

- Los **Data Writers** publican información.
    
- Los **Data Readers** reciben la información.
    
- Los datos se organizan mediante **Topics**.
    
- El descubrimiento de participantes es automático.
    

> [!info]  
> Los productores y consumidores de datos están desacoplados tanto espacial como temporalmente: no necesitan conocerse ni ejecutarse simultáneamente.

### Conceptos fundamentales

#### Domain

Un **Domain** define un espacio lógico de comunicación.

- Los participantes del mismo dominio pueden descubrirse.
    
- Participantes de dominios distintos permanecen aislados.
    

#### Participant

Representa una aplicación o proceso conectado a la red DDS.

Cada participante puede crear:

- Publicadores.
    
- Suscriptores.
    
- Topics.
    

#### Topic

Un **Topic** identifica un flujo de datos concreto.

Ejemplos:

- `/camera/image`
    
- `/imu/data`
    
- `/vehicle_attitude`
    

Un Topic está definido por:

- Nombre.
    
- Tipo de dato.
    
- Políticas de calidad de servicio.
    

#### Data Writer

Entidad encargada de publicar datos en un Topic.

#### Data Reader

Entidad encargada de recibir datos de un Topic.

### Quality of Service (QoS)

Una de las características más importantes de DDS es la posibilidad de configurar el comportamiento de la comunicación mediante políticas de **QoS**.

Algunas de las más utilizadas son:

#### Reliability

Determina si los mensajes deben entregarse obligatoriamente.

- **Best Effort**: puede perder mensajes.
    
- **Reliable**: garantiza la entrega.
    

#### Durability

Controla si los nuevos suscriptores reciben mensajes antiguos.

- Volatile.
    
- Transient Local.
    

#### History

Define cuántas muestras se almacenan.

- Keep Last.
    
- Keep All.
    

#### Deadline

Especifica el intervalo máximo esperado entre mensajes.

#### Lifespan

Establece cuánto tiempo permanece válido un mensaje.

> [!success]  
> Las QoS permiten adaptar la comunicación a las necesidades concretas del sistema: máxima fiabilidad, mínima latencia o un equilibrio entre ambas.

### Ventajas

- Arquitectura completamente distribuida.
    
- Sin servidor central.
    
- Descubrimiento automático.
    
- Escalable.
    
- Baja latencia.
    
- Configuración avanzada mediante QoS.
    
- Adecuado para sistemas críticos y de tiempo real.
    
- Independiente del lenguaje de programación.
    

### Implementaciones populares

- **Fast DDS** (eProsima).
    
- **Cyclone DDS** (Eclipse Foundation).
    
- **RTI Connext DDS**.
    
- **OpenDDS**.
    
- **CoreDX DDS**.
    

### DDS en ROS 2

ROS 2 utiliza DDS como capa de comunicación subyacente.

Esto significa que:

- Los nodos de [[ROS 2]] se descubren automáticamente.
    
- Los Topics de ROS 2 se implementan sobre DDS.
    
- Los parámetros de QoS de ROS 2 se traducen a QoS de DDS.
    
- Es posible cambiar de implementación DDS sin modificar la aplicación.
    

> [!example]  
> Cuando un nodo de [[ROS 2]] publica un mensaje en `/scan`, en realidad DDS se encarga de descubrir a los suscriptores, transportar los datos y aplicar las políticas de calidad de servicio configuradas.

### DDS y PX4

> [!info] En el ecosistema [[PX4]], DDS se utiliza para conectar el piloto automático con aplicaciones externas.

El flujo habitual es:

```text
uORB
 ↓
micro XRCE-DDS
 ↓
DDS
 ↓
ROS 2
```

Gracias a este mecanismo, los datos internos de PX4 pueden exponerse a nodos ROS 2 sin modificar el firmware del piloto automático.

## Casos de uso

- Robótica.
    
- Sistemas autónomos.
    
- Vehículos no tripulados.
    
- Sistemas aeroespaciales.
    
- Automatización industrial.
    
- Defensa.
    
- Sistemas distribuidos en tiempo real.
    
- Simulación avanzada.
    

