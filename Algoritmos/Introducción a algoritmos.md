*En este documento se detalla los distintos algoritmos de control que se han planteado para los enjambres.*


## Formación de Ejes No Coordinados Uniforme (FENCNU)

*Este tipo de allgoritmo es de los más sencillos de implementar. Parte de una posición de cada dron y actualiza todos los drones a la vez con los mismos valores, es decir, el yaw de todos gira al mismo tiempo, bloqueando la formación en una forma sin permitir su rotación.*


Este enfoque parte de que todos los drones tienen su propio eje y se manda el mismo comando de movimiento a todos. Se parte de un patrón (o formación) en el que se define la posición inicial de los drones y se manda la misma instrucción a todos. Es decir ejempplificando don el caso de dos drones:

>[!example] Ejemplo descentralizado
> Se parte de un sistema de coordenadas mundo con un origen $O=(0,0)$ y un punto dron $D=(Offset_X, Offset_Y)$ 
> 
> 
>![[Pasted image 20260623130433.png|400]]
>
>Para el caso de dos puntos-dron se ejemplificaría cada movimiento como:
>
>![[Pasted image 20260623131225.png|650]]


>[!warning] Límite del enfoque
>La utilización de este enfoque utiliza bajo coste computacional por cálculos simples que luego se paga con un límite de movimiento en la formación. La formación no podrá rotar en conjunto:
>![[Pasted image 20260623133317.png|650]]
> 
 







---
## Formación Rotable de Ejes Coordinados Uniforme Centralizada (FRECUC)
[[Enjambre_V3.py|Link al Codigo de ejemplo]]

*Este algortimo nace de un  objetivo claro, mantener la forma de la formación los drones, es decir, en caso de generar una formación en flecha, dicha formación se mantendría apuntando hacia la dirección que le comanda el yaw y no se mantendría estática como en el  FENCNU*

![[Ejes.png|450]]




