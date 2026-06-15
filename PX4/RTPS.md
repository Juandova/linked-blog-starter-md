---
tags:
  - drones/enjambre
  - drones/autopilot/PX4
date: 2026-06-04
---
> [!summary]  **Real-Time Publish-Subscribe Protocol**
> Es el protocolo de comunicación que utiliza [[DDS]] (_Data Distribution Service_) para intercambiar mensajes entre participantes de una red de forma distribuida y en tiempo real.

### ¿Qué hace RTPS?

RTPS define cómo:

- Un nodo anuncia que existe.
- Descubre otros nodos automáticamente.
- Publica datos en un tópico.
- Se suscribe a tópicos.
- Gestiona QoS (reliability, durability, deadlines, etc.).
- Serializa y transporta mensajes.

Es el equivalente a "hablar el idioma DDS en la red".