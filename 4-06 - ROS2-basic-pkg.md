---
tags:
  - MASTER/MUSANTTA
  - drones/enjambre
date: 2026-06-04
---
https://github.com/rinese89/ros2_basic_pkgs/tree/main
de Ricardo

```shell
git clone https://github.com/rinese89/ros2_basic_pkgs.git
```

```shell
cd ros2_basic_pkgs
rosdep install --from-paths . --ignore-src -r -y
colcon build
```

> [!failure] Ojo
> Realizar:
> ```shell
>source /opt/ros/humble/setup.bash
> ```

```shell title:"Para comprobar"
echo $ROS_DISTRO
```

```shell
source install/setup.bash
```

---
