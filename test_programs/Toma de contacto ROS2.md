---
tags:
  - MASTER/MUSANTTA
  - programación
  - drones/enjambre/ROS
date: 2026-06-08
---
``` title:"Estructura del workspace"
test_px4_ros_ws/
│
├── src/
│   └── px4_test_cpp/
│       ├── src/
|		|	├──	vehicle_position_listener.cpp
│       │   ├── arm_node.cpp
│       │   ├── takeoff_node.cpp
│       │   └── offboard_node.cpp
|		|	└── move_forward.cpp
│       │
│       ├── CMakeLists.txt
│       └── package.xml
│
├── build/
├── install/
└── log/
```


# Primer nodo suscriptor: [[vehicle_position_listener]]


> [!summary] Objetivo
Crear un nodo [[ROS 2]] en C++ que se suscriba a la posición local del vehículo publicada por [[PX4]].

Topic esperado:

```
/fmu/out/vehicle_local_position
```

Tipo:

```
px4_msgs::msg::VehicleLocalPosition
```

---

 > [!failure] Problemas encontrados:

## Problema 1: VS Code marca errores en los includes

Código:

```
#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>
```

VS Code mostraba:

```
cannot open source file
```

### Diagnóstico

El problema no era del código ni de ROS2.
El compilador (`colcon`) sí encontraba correctamente las dependencias.

Era únicamente un problema de IntelliSense de VS Code.

### Lección

Si:

```sh
colcon build
```

compila correctamente, los errores rojos de VS Code pueden ser únicamente problemas del editor.

Siempre distinguir entre:

- Error de compilación real.
- Error de IntelliSense.

---
## Problema 2: El nodo arrancaba pero no recibía mensajes

El nodo mostraba:

```
Vehicle Position Listener iniciado
```

pero nunca entraba en el callback.

### Diagnóstico

El topic utilizado era:

```
/fmu/out/vehicle_local_position
```

Sin embargo [[PX4]] estaba publicando:

```
/fmu/out/vehicle_local_position_v1
```

### Causa

Las versiones recientes de PX4 DDS añaden sufijos de versión:

```
_v1
_v2
_v3
_v4
```

para mantener compatibilidad entre diferentes versiones de mensajes.

### Solución

Suscribirse al topic correcto:

```
"/fmu/out/vehicle_local_position_v1"
```

### Lección

Nunca asumir el nombre del topic.

Comprobar siempre:

```sh
ros2 topic list
```

antes de escribir código.

---
## Problema 3: Incompatibilidad QoS

Después de corregir el topic apareció:

```
New publisher discovered on topic ...
offering incompatible QoS

Last incompatible policy:
RELIABILITY_QOS_POLICY
```

### Diagnóstico

PX4 publicaba:

```
BEST_EFFORT
```

El nodo ROS2 escuchaba:

```
RELIABLE
```

DDS rechazó la conexión.

---

### Qué es QoS

QoS significa:

```
Quality of Service
```

Define las reglas de comunicación entre publicadores y suscriptores DDS.

Ejemplos:

- Fiabilidad
- Historial
- Durabilidad
- Profundidad de cola

---

#### BEST_EFFORT

Significa:

```
"Entrega los datos si puedes."
```

Si se pierde un paquete:

```
No se retransmite.
```

Ventajas:

- Menor latencia.
- Menor carga de red.
- Adecuado para sensores de alta frecuencia.

Ejemplos:

```
vehicle_attitude
vehicle_odometry
vehicle_local_position
sensor_combined
```

PX4 usa BEST_EFFORT en muchos topics de telemetría.

---

#### RELIABLE

Significa:

```
"Debes entregar el mensaje."
```

Si un paquete se pierde:

```
DDS solicita retransmisión.
```

Ventajas:

- Mayor robustez.

Desventajas:

- Mayor latencia.
- Más tráfico.

Adecuado para:

```
comandos
configuración
eventos importantes
```

---

### Solución aplicada

Crear explícitamente un QoS compatible:

```
auto qos = rclcpp::QoS(rclcpp::KeepLast(10));
qos.best_effort();
```

y usarlo en la suscripción.

---

## Cómo inspeccionar el QoS de un topic

Comando:

```sh
ros2 topic info -v /fmu/out/vehicle_local_position_v1
```

Salida relevante:

```
Publisher:
  Reliability: BEST_EFFORT

Subscriber:
  Reliability: RELIABLE
```

Esto explica inmediatamente por qué la comunicación falla.

---
## Lecciones aprendidas

Antes de escribir un nodo [[ROS 2]] para [[PX4]]:

1. Verificar que el topic existe.

```sh
ros2 topic list
```

2. Verificar el tipo.

```sh
ros2 topic info <topic>
```

3. Verificar el QoS.

```sh
ros2 topic info -v <topic>
```

4. Comprobar la definición del mensaje.

```sh
ros2 interface show px4_msgs/msg/...
```

---
## Resultado final

El nodo recibe correctamente:

```
msg->x
msg->y
msg->z
```

desde:

```
/fmu/out/vehicle_local_position_v1
```

utilizando un QoS compatible con PX4.

---
# Primer nodo publisher: [[arm_node]]

##### Comprobaciones previas

```sh 
ros2 topic info /fmu/in/vehicle_command
ros2 topic info /fmu/out/vehicle_command_ack_v1
```

y 

```sh 
ros2 interface show px4_msgs/msg/VehicleCommand
```

donde nos interesa ver:
```
VEHICLE_CMD_COMPONENT_ARM_DISARM = 400
ARMING_ACTION_DISARM = 0
ARMING_ACTION_ARM = 1
```

---

## Problema 1

```sh title:"Terminal 1"
$ ros2 run px4_test_cpp arm_node
[INFO] [1780759177.331748185] [arm_node]: Arm node iniciado
[INFO] [1780759178.332071568] [arm_node]: Comando ARM enviado
```

```sh title:"Terminal 2"
$ ros2 topic echo /fmu/out/vehicle_command_ack_v1
timestamp: 1780759178344841
command: 400
result: 1
result_param1: 0
result_param2: 0
target_system: 1
target_component: 1
from_external: false
---
```

> [!failure]  No se arma

#### Lo primero: el comando sí llegó

Sabemos que:

```
ROS2 ↓vehicle_command ↓PX4
```

funciona.

Si no llegara, no habría ACK.

---

#### Lo segundo: PX4 lo rechazó

El ACK indica:

```
result: 1
```

En PX4/MAVLink normalmente:

```
0 = ACCEPTED1 = TEMPORARILY_REJECTED2 = DENIED3 = UNSUPPORTED...
```

Por tanto:

```
TEMPORARILY_REJECTED
```

---

#### Lo tercero: el dron sigue desarmado

Vemos:

```
arming_state: 1
```

Lo importante es que:

```
armed_time: 0
```

sigue siendo cero.

Y además:

```
takeoff_time: 0
```

también.

Por tanto el armado nunca ocurrió.

----

