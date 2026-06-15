---
tags:
  - MASTER/MUSANTTA
  - programación/robótica
  - drones/enjambre/ROS
date: 2026-06-08
---
```C++ title:"vehicle_position_listener.cpp"
#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>

class VehiclePositionListener : public rclcpp::Node
{
public:
    VehiclePositionListener()
    : Node("vehicle_position_listener")
    {
        auto qos = rclcpp::QoS(rclcpp::KeepLast(10));
        qos.best_effort();

        subscription_ =
            this->create_subscription<px4_msgs::msg::VehicleLocalPosition>(
                "/fmu/out/vehicle_local_position_v1",
                qos,
                std::bind(
                    &VehiclePositionListener::position_callback,
                    this,
                    std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(),
                    "Vehicle Position Listener iniciado");
    }

private:
    void position_callback(const px4_msgs::msg::VehicleLocalPosition::SharedPtr msg)
    {
        RCLCPP_INFO(
            this->get_logger(),
            "Posición -> x: %.2f  y: %.2f  z: %.2f",
            msg->x,
            msg->y,
            msg->z);
    }

    rclcpp::Subscription<
        px4_msgs::msg::VehicleLocalPosition>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);

    auto node = std::make_shared<VehiclePositionListener>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}
```

---
# [[ROS 2]] + [[PX4]]: Anatomía de mi primer nodo suscriptor

> [!summary]  
> Este nodo crea un objeto ROS2 capaz de escuchar el topic `/fmu/out/vehicle_local_position_v1` publicado por [[PX4]]. Cuando llega un mensaje nuevo, [[ROS 2]] ejecuta automáticamente una función (_callback_) que imprime la posición local del dron (`x`, `y`, `z`). El nodo utiliza un perfil QoS `BEST_EFFORT` para ser compatible con la configuración [[DDS]] utilizada por [[PX4]].

---

```
main()
  ↓
crea nodo
  ↓
crea suscripción
  ↓
spin()
  ↓
espera eventos
  ↓
callback()
```

## Visión global

El flujo completo es:

```
PX4
 ↓
VehicleLocalPosition
 ↓
DDS
 ↓
ROS2 Topic
 ↓
Subscription
 ↓
Callback
 ↓
Consola
```

Cada vez que PX4 publica una nueva posición:

```
x = 1.23
y = 0.54
z = -2.01
```

ROS2 recibe el mensaje y ejecuta automáticamente:

```cpp
position_callback(...)
```

---

## Includes

```cpp
#include <rclcpp/rclcpp.hpp>
#include <px4_msgs/msg/vehicle_local_position.hpp>
```

#### rclcpp

```cpp
#include <rclcpp/rclcpp.hpp>
```

Carga la librería principal de ROS2 para C++.

Permite utilizar:

- Nodos
- Publicadores
- suscriptores
- Timers
- Logs
- QoS

Sin esta librería no existe ROS2 dentro del programa.

---
#### [[px4_msgs]]

```cpp
#include <px4_msgs/msg/vehicle_local_position.hpp>
```

Importa la definición del mensaje:

```cpp
px4_msgs::msg::VehicleLocalPosition
```

Gracias a esto el compilador conoce los campos:

```cpp
msg->x
msg->y
msg->z
msg->vx
msg->vy
msg->vz
```

Sin este `#include` ROS2 no sabría interpretar los datos enviados por PX4.

---
## Clase principal

```cpp
class VehiclePositionListener : public rclcpp::Node
```

Aquí se crea una nueva clase.

Hereda de:

```cpp
rclcpp::Node
```

Es decir:

```
VehiclePositionListener
       es un
       Node
```

Todo nodo ROS2 suele derivar de:

```cpp
rclcpp::Node
```

---
## Constructor

```cpp
VehiclePositionListener()
: Node("vehicle_position_listener")
```

El constructor se ejecuta una única vez cuando se crea el nodo.

La línea:

```cpp
Node("vehicle_position_listener")
```

asigna el nombre ROS2:

```
vehicle_position_listener
```

Puede verse con:

```sh
ros2 node list
```

---

### Configuración QoS

```cpp
auto qos = rclcpp::QoS(rclcpp::KeepLast(10));
```

Se crea un perfil QoS.

Significa:

```
Guardar los últimos 10 mensajes.
```

Si llegan más:

```
11
12
13
...
```

los antiguos se descartan.

---

```cpp
qos.best_effort();
```

Configura:

```
Reliability = BEST_EFFORT
```

Equivale a:

```
"Entrégame los datos si puedes."
```

Si se pierde un paquete:

```
No se retransmite.
```

Esto es compatible con la mayoría de topics publicados por PX4.

---
### Creación de la suscripción

```cpp
subscription_ =
    this->create_subscription<
        px4_msgs::msg::VehicleLocalPosition>(
```

Esta línea crea un suscriptor.

ROS2 entiende:

```
Quiero escuchar mensajes
de tipo VehicleLocalPosition.
```

---
#### Topic

```cpp
"/fmu/out/vehicle_local_position_v1"
```

Es el nombre del topic [[DDS]].

[[ROS 2]] se conecta exactamente a esa fuente de datos.

> [!important] Importante:
> El nombre debe coincidir exactamente.
> Si el topic no existe: No se recibe nada.

---
#### Callback

```cpp
std::bind(
    &VehiclePositionListener::position_callback,
    this,
    std::placeholders::_1)
```

Esta línea indica:

```
Cuando llegue un mensaje,
ejecuta position_callback().
```

ROS2 almacena internamente esta referencia.

No se ejecuta ahora.
Se ejecutará en el futuro.

---

##### Qué es un callback

> [!abstract] Un callback es una función que ROS2 llama automáticamente cuando ocurre un evento.

En este caso:

```
Evento:
Llegó un mensaje nuevo.
```

Acción:

```cpp
position_callback(...)
```

---
#### Log de inicio

```cpp
RCLCPP_INFO(
    this->get_logger(),
    "Vehicle Position Listener iniciado");
```

Imprime:

```
Vehicle Position Listener iniciado
```

solo una vez.

Sirve para verificar que el nodo arrancó correctamente.

---

### Función Callback

```cpp
void position_callback(const px4_msgs::msg::VehicleLocalPosition::SharedPtr msg)
```

Esta función recibe un mensaje enviado por PX4.

La variable:

```cpp
msg
```

contiene todos los campos del mensaje.

Por ejemplo:

```cpp
msg->x
msg->y
msg->z
```

---

#### SharedPtr

```cpp
SharedPtr msg
```

Es un puntero inteligente.

ROS2 utiliza este mecanismo para evitar copias innecesarias de memoria.

Conceptualmente puede verse como:

```text
msg
 ↓
mensaje recibido
```

---
#### Lectura de datos

```cpp
msg->x
msg->y
msg->z
```

Acceden a los campos del mensaje.

Por ejemplo:

```text
x = 3.1
y = 1.2
z = -2.0
```

---
#### Mostrar datos

```cpp
RCLCPP_INFO(
    this->get_logger(),
    "Posición -> x: %.2f y: %.2f z: %.2f",
    msg->x,
    msg->y,
    msg->z);
```

Imprime la posición en consola.

Ejemplo:
``` 
Posición -> x: 1.52 y: -0.43 z: -2.01
```

---
### Variable miembro

```cpp
rclcpp::Subscription<
    px4_msgs::msg::VehicleLocalPosition>::SharedPtr
    subscription_;
```

> [!important] Guarda la suscripción.

Si no se almacenara:

```cpp
create_subscription(...)
```

se destruiría al terminar el constructor.

Entonces ROS2 dejaría de recibir mensajes.

---
## Función main

```cpp
int main(int argc, char * argv[])
```

Es el punto de entrada del programa.

---
### Inicializar ROS2

```cpp
rclcpp::init(argc, argv);
```

> [!info]  Inicializa ROS2.
> Sin esta llamada nada de ROS funcionaría.

---
### Crear el nodo

```cpp
auto node =
    std::make_shared<VehiclePositionListener>();
```

> [!info] Construye el objeto.

Aquí se ejecuta:
```cpp
VehiclePositionListener()
```

---

### Bucle principal

```cpp
rclcpp::spin(node);
```

> [!info] Es probablemente la línea más importante del programa.
> Significa:
> 1. Mantén vivo el nodo.
> 2. Espera eventos.
> 3. Ejecuta callbacks.

Mientras el programa permanezca aquí:

```
ROS2 escucha mensajes.
```

---
## Finalizar ROS2

```cpp
rclcpp::shutdown();
```

> [!info] Libera recursos cuando el programa termina.

---

## Modelo mental correcto


```
ROS2 espera mensajes.

Cuando llega uno:

    ejecuta callback()

Cuando llega otro:

    ejecuta callback()
```

Es una arquitectura dirigida por eventos (_event-driven_).

----
