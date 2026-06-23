---
tags:
  - drones/enjambre/ROS
  - MASTER/MUSANTTA/Practicas
date: 2026-06-23
---
> [!summary]  Responsabilidad:
> calcular el vector distancia de cada dron respecto al centroide



## Topics


### Topics creado:

`swarm_pkg/msg/Formation.msg`

```
uint32 num_drones  
  
float32[] x  
float32[] y  
float32[] z
```


`drone_N/out/formation`

## Responsabilidades


> [!example] Dada una formación:  
> - Matrix  
> - Delta  
> - Linea
> - Cubo
> - Hexagono
> - Logo de MUSANTTA
> - etc
> 
> Calcula los vectores de distancia(o offsets) de cada dron al centroide. 

``` title:Ejemplo
Centroide = ( 0, 0,0)
Drone0    = (-2,+2,0)
Drone1    = ( 0,+2,0)
Drone2    = (+2,+2,0)
Drone3    = (-2, 0,0)
Drone4    = ( 0, 0,0)
Drone5    = (+2, 0,0)
```

