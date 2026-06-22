



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


----

## Responsabilidad

`manual_swarm_control` proporciona una interfaz de control manual para un enjambre de drones utilizando el teclado.

Su función es actuar como un operador humano capaz de:

- Seleccionar uno o varios drones.
    
- Enviar órdenes de despegue y aterrizaje.
    
- Desplazar drones en el espacio.
    
- Modificar orientación.
    
- Realizar pruebas rápidas del sistema sin necesidad de implementar todavía algoritmos de formación.
    

---

## Arquitectura

```
            Teclado
               │
               ▼
    manual_swarm_control
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
   drone_0  drone_1  drone_2
```

---

## Parámetros

```sh
ros2 run swarm_pkg manual_swarm_control --ros-args -p num_drones:=3
```

|Parámetro|Descripción|
|---|---|
|num_drones|Número de drones que forman el enjambre|

---

## Interfaces ROS

### Action Clients

```
/drone_N/action/takeoff
/drone_N/action/land
```

### Publishers

```
/drone_N/in/target_pose
```

Tipo:

```
swarm_pkg/msg/DronePose
```

### Subscribers

```
/drone_N/out/pose
```

Tipo:

```
swarm_pkg/msg/DronePose
```

---

## Selección de drones

```
0 -> Todos los drones

1 -> drone_0
2 -> drone_1
3 -> drone_2
...
```

---

## Controles

```
t -> Takeoff
l -> Land

w -> Avanzar
s -> Retroceder

a -> Desplazamiento izquierda
d -> Desplazamiento derecha

r -> Subir
f -> Bajar

q -> Rotar izquierda
e -> Rotar derecha

+ -> Aumentar velocidad
- -> Reducir velocidad

h -> Mostrar ayuda

ESPACIO -> Stop
```

---

## Sistema de referencia

Los movimientos se realizan respecto al heading actual del dron.

Ejemplo:

```
yaw = 0 rad
```

```
W -> +X
S -> -X
```

```
yaw = π/2 rad
```

```
W -> +Y
S -> -Y
```

Por tanto:

```
W = avanzar hacia donde mira el dron
```

independientemente de su orientación global.