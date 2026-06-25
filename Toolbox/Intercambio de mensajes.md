
"~/Desktop/QGroundControl*.AppImage",


1. Configurar la velocidad del puerto [[1](https://www.tormentadebits.com/2017/07/lectura-de-puerto-serial-en-os-unix-like.html)]

Abre tu terminal y utiliza `stty` indicando el puerto y la velocidad deseada. Por ejemplo, para configurar `/dev/ttyUSB0` a 9600 baudios: [[1](https://www.tormentadebits.com/2017/07/lectura-de-puerto-serial-en-os-unix-like.html)]

`sudo stty -F /dev/ttyUSB0 9600`

2. Leer datos del puerto con `cat`

Una vez configurado correctamente Comando stty de Linux con Ejemplos Prácticos, puedes usar `cat` para empezar a visualizar el flujo de datos en tiempo real:

`cat /dev/ttyUSB0` [[1](https://www.tlm.unavarra.es/~daniel/docencia/lpr/lpr08_09/practicas/practica1.pdf)]


```sh title:"Utiles"
sudo fuser -v /dev/ttyUSB0
```

src/px4_msgs/

src/px4_ros_com/

build/

install/

log/

.vscode/

---
```sh 
$ ros2 interface proto px4_msgs/msg/HomePosition
"timestamp: 0
lat: 0.0
lon: 0.0
alt: 0.0
x: 0.0
y: 0.0
z: 0.0
roll: 0.0
pitch: 0.0
yaw: 0.0
valid_alt: false
valid_hpos: false
valid_lpos: false
manual_home: false
update_count: 0


```

ros2 topic echo /px4_1/fmu/out/home_position_v1