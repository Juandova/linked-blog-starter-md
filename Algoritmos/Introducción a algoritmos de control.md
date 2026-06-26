*En este documento se detalla los distintos algoritmos de control que se han planteado para los enjambres.*


## Formación de Ejes No Coordinados Uniforme (FENCNU)

*Este tipo de allgoritmo es de los más sencillos de implementar. Parte de una posición de cada dron y actualiza todos los drones a la vez con los mismos valores, es decir, el yaw de todos gira al mismo tiempo, bloqueando la formación en una forma sin permitir su rotación.*

Esta filosofía parte de que todos los drones tienen su propio eje y se manda el mismo comando de movimiento a todos. Se parte de un patrón (o formación) en el que se define la posición inicial de los drones y se manda la misma instrucción a todos. Es decir ejempplificando don el caso de dos drones:

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


>[!example] Ejemplo de control centralizado
>Se parte de un centroide que mantiene las posiciones a cierda distancia $r$ con un ángulo $\alpha$ . 
>
![[Ejes.png|450]]
>
>Las coordenadas x e y, del punto se podrán calcular con senos y cosenos:
>
>![[Pasted image 20260625135203.png]]
>
>$$\huge{p\rightarrow\begin{cases}x = r\cos{\alpha} \\ y=r\sin{\alpha} \end{cases}}$$
>
>Pero tras el cambio de punto con respecto al centroide es necesario realizar una transformación de la posición.
>
>![[Pasted image 20260625135743.png]]
>
>Por lo tanto, por relación de distribución:
 $$\huge{p'\rightarrow\begin{cases}x' = r\cos{(\alpha+\beta)} \\ y'=r\sin{(\alpha+\beta)} \end{cases}}$$
 >
 >$$\huge{p'\rightarrow\begin{cases}x' = r(\cos{(\alpha)}·cos{(\beta)}-\sin{(\alpha)}·\sin{(\beta)}) \\ y'=r(\sin{(\alpha)}·\sin{(\beta)}+\cos{(\alpha)}·\sin{(\beta)}) \end{cases}}$$
 >
 >Partiendo de la posición anterior el cálculo $\large{x = r\cos{\alpha}}$ e $\large{y=r\sin{\alpha}}$ :
 >
 $$\huge{p'\rightarrow\begin{cases}x' = r(x·\cos{(\beta)}-y·\sin{(\beta)}) \\ y'=r(y·\sin{(\beta)}+x·\cos{(\beta)})\end{cases}}$$
 >
 >Es decir, una transformada de rotación multiplicada al offset de las distancias:
 >$$\large{\begin{pmatrix}{x'}\\{y'} \end{pmatrix}=\begin{pmatrix}{cos\beta }{-sin\beta}\\{sin\beta} {cos\beta} \end{pmatrix}· \begin{pmatrix}{x}\\{y}\end{pmatrix}}$$
 >
 >Con este cambio en el cálculo de las posiciones se consigue rotar toda la formación en bloque:
 >
 >![[Pasted image 20260625153837.png]] 
