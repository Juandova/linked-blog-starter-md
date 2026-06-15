Para la creación de toda la documentación se ha hecho uso de los tutoriales de la web[W3School](https://www.w3schools.com/git/#) y la [ documentación oficial de Git](https://git-scm.com/docs).

## Introducción
En este apartado se asume que ya se conocen los conceptos con los que trabaja Git (Stage, Push, Pull...) y se ha configurado el entorno con nombre y correo. En caso contrario leer [[Introducción a Git]].

Este documento tratará los aspectos más básicos de control de versiones de repositorio hasta un WorkFlow recomendado y buenas prácticas de uso.

## Inicio

**Objetivos:**
- Crear una carpeta de proyecto
- Navegar por la carpeta
- Inicializar un repositorio en git

**Para crear una carpeta** se hará uso de los comandos básicos de Linux sobre bash a la dirección en la que se desea crear.

```sh 
mkdir myproject
cd myproject
```

El primer comando crea el directorio de trabajo, mientras el segundo lo abre dentro de la barra de comandos.

**Para crear el repositorio** dentro de la carpeta es tan sencillo como navegar por la terminal hasta la carpeta en la que se desea crear y utilizar el comando `git init'.

```sh
git init
```

>[!info] Directorios en Linux 
Por defecto Linux nos lleva a la carpeta `Home`, a la que se accede desde la terminal por defecto y se muestra como **~**, es decir, `Nombre1@Nombre2:~$`, sin embargo la carpeta raíz en Linux es **/** por lo que si se aplica el comando `cd /`se accede a `Nombre1@Nombre2:/`, dese ahí la ruta a `/home/usuario`  es  `cd home` y se puede utilizar ls para ir listando en la terminal los directorios disponibles. 

Tras iniciar el git en nuestro respositorio se puede observar la carpeta oculta que se ha generado con el comando ls -a, apareciendo tres carpetas nuevas ocultas: `. .. .git`.

## Nuevos archivos con git

- [ ] Mejorable, poner ejemplo creando un repositorio o un archivo

 Un nuevo archivo para git, es un archivo que creas o copias dentro de tus archivos pero no le has avisado a git para que revise.  Para obtener la información de git en la carpeta designada para el repositorio se utiliza el siguiente comando:

```sh
git status
```

Por ejemplo, para un repositorio en el que se acaba de hacer git init y ya poseía carpetas con archivos:
```sh title:"Ejemplo de respuesta en bash con una carpeta creada:"
alejandro@Juando:~/ros2_ws$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	build/
	install/
	log/
	ros_tutorials/
	src/

nothing added to commit but untracked files present (use "git add" to track)
```

Se muestra las cinco carpetas del repositorio pero git no está haciendo seguimiento de ninguna de ellas ni sus archivos. Es decir, git no guarda los cambios de aquellos archivos a los que no se le haya indicado que tiene que seguir. 

## Stage Environment (Establecimiento de entorno)

Un stage es similar a una sala de espera para los cambios. Se utiliza para decirle a Git exactamente qué archivos se desea incluir en el siguiente commit

