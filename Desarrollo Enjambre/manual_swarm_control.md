



```sh 
ros2 run swarm_pkg manual_swarm_control --ros-args -p num_drones:=3
```


---

El `manual_swarm_control` será cliente de:

```
/drone_N/action/takeoff/drone_N/action/land
```

y publicador de:

```
/drone_N/in/target_pose/drone_N/in/target_yaw
```

y suscriptor de:

```
/drone_N/out/pose
```

