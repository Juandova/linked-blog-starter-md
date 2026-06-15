---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre
date: 2026-06-06
---
> [!summary]  px4_msgs
> es el **paquete de [[ROS 2]] que contiene las definiciones de mensajes (interfaces `.msg`) utilizadas por [[PX4]] para intercambiar datos con [[ROS 2]]**.

- PX4 publica información interna (posición, actitud, sensores, estado de la batería, etc.).
- ROS 2 necesita conocer exactamente la estructura de esos datos.
- `px4_msgs` proporciona esas estructuras de datos en formato ROS 2.

Sin `px4_msgs`, ROS 2 no sabría interpretar los mensajes que envía PX4 ni podría enviar comandos que PX4 entienda


---

```C++ title:"Ejemplo de uso"
auto sub =
node->create_subscription<
    px4_msgs::msg::VehicleOdometry>(
    "/fmu/out/vehicle_odometry",
    10,
    callback);
```

---
### Instalación

[ROS 2 User Guide](https://docs.px4.io/main/en/ros2/user_guide)

```sh title:"Clone repository github"
mkdir -p ~/utiles_px4_ws/src/
cd ~/utiles_px4_ws/src/
git clone https://github.com/PX4/px4_msgs.git
```

### Compilación

```sh title:"Compilación px4_msgs"
cd ~/utiles_px4_ws/
colcon build
source install/setup.bash
```

> [!failure]  Puede dar errores con el setup  tools y el packagess
> se resuelve compatiblizando ambas versiones

---
## Documentación

- [PX4_msgs GitHub](https://github.com/PX4/px4_msgs)