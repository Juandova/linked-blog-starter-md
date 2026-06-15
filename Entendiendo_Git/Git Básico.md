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
[Link a la referencia](https://www.w3schools.com/git/git_new_files.asp?remote=github)
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
[Link a la referencia](https://www.w3schools.com/git/git_staging_environment.asp?remote=github)
- [ ] Mejorable, poner ejemplo creando estableciendo un archivo en el entorno y extrayendolo después

Un stage es similar a una sala de espera para los cambios. Se utiliza para decirle a Git exactamente qué archivos se desea incluir en el siguiente commit, así se controla todo el historial del proyecto.

**Los comandos básicos son:**
- `git add <file>` - Para añadir un archivo
- `git add --all` or `git add -A` - Para añadir todos los archivos/cambios de la carpeta
- `git status` - Para ver los archivos establecidos y cambios
- `git restore --staged <file>` - Para quitar un archivo del establecimiento de entorno

## Commits
[Link a la referencia](https://www.w3schools.com/git/git_commit.asp?remote=github)
Un *commit* es un punto de guardado en tu proyecto. Hace un guardado instantáneo junto con un mensaje que indica los cambios realizados. Siempre puedes volver atrás a un *commit* previo si lo necesitas. 

**Los comandos básicos son:** 
- `git commit -m "message"` - Cambios de un commit establecido con un mensage (preferiblemente descriptivo)
- `git commit -a -m "message"` - Hace un commit a todos los cambios seguidos (Se salta el establecimiento).
- `git log` - Para ver el historial de cambios
- `git log --oneline` -Versión más corta del log en una línea.
- `git log --stat` -Muestra los archivos cambiados en el último commit.

Puedes saltar los establecimientos para aquellos **archivos que ya han sido previamente establecidos** con `git commit -a -m "message"`.  
*Este paso puede llevar a cambios no deseados y no funciona para archivos no establecidos ni nuevos.*

En caso de no usar el -m se abre un editor con diferentes líneas. Se puede hacer un resumen corto en la primera línea, después se deja una línea vacía y se añaden más detalles debajo.

#### Buenas prácticas a la hora de hacer commit:
- Primera línea corta (50 caracteres o menos).
- Usar el imperativo y no el pasdo (ej: "Se añade una función" y no "Se ha añadido una función").
- Dejar un espacio en blanco tras la primera línea de resumen.
- Describir por qué se ha realizado un cambio y no únicamente qué se ha cambiado.
#### Otras opciones útiles de commit:
- **Crear un commit vacío:**  
    `git commit --allow-empty -m "Start project"`
- **Utilizar un mensaje de commit previo (sin el editor):**  
    `git commit --no-edit`
- **Añadir rápidadmente los cambios en establecimiento al último commit manteniendo el mensaje anterior:**  
    `git commit --amend --no-edit`
- **Se te ha olvidado establecer un archivo?**  
    Si utilizas `git commit -m "message"` pero se te ha olvidado hacer `git add` a un archivo, simplemente añadelo y haz el commit otra vez. O podrías utilizar `git commit --amend` para añadirlo rápidamente al último commit.
- **Una falta de ortografía en la descripción del cambio?**  
    Utiliza `git commit --amend -m "Corrected message"` para arreglarlo.
- **Has hecho commit de un archivo erróneo?**  
    Puedes utilizar `git reset --soft HEAD~1` para deshacer el útlimo commit manteniendo los cambios establecidos.

## Tags
[Link a la referencia](https://www.w3schools.com/git/git_tagging.asp?remote=github)
Un tag en git es como una etiqueta o un marcador para un commit en específico. Los tags se utilizan normalmente para marcar puntos importantes en el historial del proyecto como versiones (v1.0, v2.0...). Los tags son una manera simple y efectiva de mantener un seguimiento de las versiones y compartirlas con el resto de usuarios o miembros de un equipo.

Un **lightweight tag** o "etiqueta ligera" es simplemente un nombre para un commit. Es rápido, y simple pero añade información que puede ser clave. Un **annotated tag** en cambio guarda otros datos como autor, fecha y mensaje. Es recomendable si se trabaja con un equipo de personas.

Los comandos en este apartado son:
- `git tag <tagname>` - Crea un  "lightweight tag"
- `git tag -a <tagname> -m "message"` - Crea un "annotated tag"
- `git tag <tagname> <commit-hash>` -Añade un tag a un commit específico
	*(El hash se puede obtener con el comando ``git log --oneline``)*
- `git tag` - List tags
- `git show <tagname>` - Show tag details
- `git tag -d <tagname>` - Elimina el tag

Por defecto, las tags únicamente aparecen en tu ordenador. Para que otros puedan verlo se deberá hacer un "push". Para subir un tag:

```shell title:"Subir un tag"
git push origin v1.0
```

Para subirlos todos:
```shell title:"Subir todos los tags"
git push --tags
```

## Stash
[Link a la referencia](https://www.w3schools.com/git/git_stash.asp?remote=github)
(No me parece una herramienta particularmente útil)
Un stash permite rápidamente cambiar entre tareas o arreglar un bug pero el trabajo no está listo para hacer un commit. Un stash permite esconder los cambios a los que no se ha aplicado un commit y volver a un directorio limpio. Puedes volver atrás para reestablecer los cambios posteriormente.

Casos de uso:
- **Cambiar de rama de manera segura:** Guarda el trabajo antes de cambiar de rama
- **Manejo de emergencias:** Se puede hacer un stash para hacer un arreglo urgente y luego restaurarlo.
- **Mantener el trabajo  en progreso seguro:** Evita commits innecesarios o pérdida de cambios.


