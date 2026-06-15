---
tags:
  - MASTER/MUSANTTA
  - enjambres
date: 2026-05-07
---
> [!abstract]
> Esta nota documenta el proceso para instalar el entorno de desarrollo de PX4 Autopilot en Windows utilizando WSL. Incluye:
> - Instalación de [[WSL]]
> - Instalación de [[PX4]]
> - Instalación y conexión con [[QGroundControl]]
> - Integración con MatLab

---
# 1. Instalar WSL

> [!info] **WSL** permite ejecutar Linux dentro de Windows.

1. Abrir **PowerShell como Administrador** y ejecutar:



```powershell
wsl --install
```

- Verificar instalación

```powershell
wsl --version
```

2. Iniciar WSL

```powershell
wsl
```

3. Crear usuario de ubuntu
4. Actualizar ubuntu

```shell
cd ~
sudo apt update && sudo apt upgrade -y
```

# 2. Descargar repositorio PIX4

- Se necesita la función `git`

```shell
sudo apt install git -y
```

- Verificar instalación

```shell
git --version
```

1. Clonar el repositorio PIX4, junto con sus submódulos:
	- Repositorio oficial:
		- [https://github.com/PX4/PX4-Autopilot](https://github.com/PX4/PX4-Autopilot)

```shell
git clone --recursive https://github.com/PX4/PX4-Autopilot.git
```

2. Instalar dependencias 

```shell 
bash ./Tools/setup/ubuntu.sh
```

- Reiniciar

```shell
sudo reboot
```

Volver a iniciar:
```powershell
wls
```

3. Compilar
	- Se necesita la función `make` \*

```shell
cd PX4-Autopilot
make px4_sitl
```

- \* instalar `make`

```shell
sudo apt install make
```

- Ejecutar simulación Gazebo

```shell
make px4_sitl gz_x500
```
# 3. Instalar QGroundControl

Descarga oficial: [QGroundControl Downloads](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html)
- Se instala tambien el UAVdrivers
# 4. Conectar PX4 con QGroundControl

1. Ejecuta QGroundControl
2. Lanza en diferentes terminales:

```shell title:"DRON 1º"
cd ~\PX4-Autopilot
PX4_HOME_LAT=39.48053 PX4_HOME_LON=-0.33928 PX4_HOME_ALT=10 make px4_sitl gz_x500
```

```shell title:"DRON 2"
cd ~\PX4-Autopilot
PX4_SIM_MODEL=gz_x500 PX4_GZ_MODEL_POSE="3,0,0,0,0,0" ./build/px4_sitl_default/bin/px4 -i 1
```

```shell title:"DRON 3"
cd ~\PX4-Autopilot
PX4_SIM_MODEL=gz_x500 PX4_GZ_MODEL_POSE="6,0,0,0,0,0" ./build/px4_sitl_default/bin/px4 -i 2
```

Con `-i N` crea una **instancia SITL independiente** de PX4.  
Esta instancia modifica automáticamente varios recursos para evitar colisiones entre vehículos:
- puertos UDP/TCP
- directorios de trabajo
- nombres de instancia
- MAVLink system ID (`MAV_SYS_ID`)
- namespaces internos
- sockets de simulación

De esta forma los puertos para cada simulación se queda:

| Instancia | Puerto |
| --------- | ------ |
| 0         | 18570  |
| 1         | 18571  |
| 2         | 18572  |
```shell
param show MAV_SYS_ID
```

---

Para saber cual es la IP local asignada a la maquina virtual:

```shell
ip route
```

Respuesta: `default via 172.17.64.1 dev eth0 proto kernel`
`172.17.64.0/20 dev eth0 proto kernel scope link src 172.17.74.42`

La IP del entorno virtual es: `172.17.74.42`

---
En **QGroundControl**, en el apartado de Comm Links de Applications Settings se agregan nuevas conexiones manuales con Add New Link para cada simulación de dron, y se desactivan todas las conexiones automáticas. 

Para cada nueva conexión se selecciona Type UDP y se introduce el Port ``14550``, y en ServerAdress:

| Drone   | Server               |
| ------- | -------------------- |
| Drone 1 | `172.xx.xx.xx:18570` |
| Drone 2 | `172.xx.xx.xx:18571` |
| Drone 3 | `172.xx.xx.xx:18572` |

---
# 5. Matlab

- versión R2024b o superior

- Instalar 
	- [UAV Toolbox](https://es.mathworks.com/products/uav.html)
		- Licencia: **1.085 €** per year
	- Signal Processing Toolbox


1. Hay qué configurar lo siguiente en el QGroundControl:
	1. Activar el MAVlink Forwarding
		- En Application Settings / Telemetry
	2. Activar el modo Offboard en los Drones 2 y 3
		1. Click en el modo de vuelo (Hold por defecto)
			- Aparecerá una lista de modos de vuelo
			- Si no aparece, click en la flechita y activar el Edit Displayed Flight Modes
			- Si sigue sin aparecer aquí, click en Flight Mode Configure
				- En Flight Mode 1 seleccionar OffBoard
				- Cambiar con el dron desarmado
		- El Dron 1 se mantiene en Hold
2. En el código MatLab Simulink: Crear la variable t con valor 100
3. con los drones en vuelo y los drones 2 y 3 en modo Offboard, ejecutar el código de MatLab Simulink