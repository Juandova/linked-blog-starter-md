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
	- (utilizando `/` seguido de la búsqueda y luego presionando enter se puede hacer una búsqueda de los commits, `n` se puede utilizar para buscar la siguiente coincidencia. Para salir se puede utiliza q) 
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

## Stash (Esconder)
[Link a la referencia](https://www.w3schools.com/git/git_stash.asp?remote=github)

*(No me parece una herramienta muy importante)*

Un stash permite rápidamente cambiar entre tareas o arreglar un bug pero el trabajo no está listo para hacer un commit. Un stash permite esconder los cambios a los que no se ha aplicado un commit y volver a un directorio limpio. Puedes volver atrás para reestablecer los cambios posteriormente.

Casos de uso:
- **Cambiar de rama de manera segura:** Guarda el trabajo antes de cambiar de rama
- **Manejo de emergencias:** Se puede hacer un stash para hacer un arreglo urgente y luego restaurarlo.
- **Mantener el trabajo  en progreso seguro:** Evita commits innecesarios o pérdida de cambios.

- `git stash` - Esconde  los cambios en un stash
- `git stash push -m "message"` - Igual al anterior pero con un mensaje
- `git stash list` - Muestra todos los stashes
- `git stash branch <branchname>` - Crea una rama a partir de un stash
-  `git stash show` muestra el cambio realizado en el último stash.  Para mostrar las líneas exactas que han cambiado desde el último stash se puede utilizar ``git stash show -p``.

Los cambios realizados se guardan en un "Stack" , es decir, se van apilando unos encima de otros, siendo el más reciente el que está por encima y va bajando.

 Otros comandos:

- `git stash apply`- Reestablece los cambios del último stash manteniendo el stash en el stack.
- ` git stash apply stash@{n}`- Permite reestablecer un stash específico
- `git stash pop`- Aplica el último stash y lo elimina del stack
- `git stash drop`- Elimina un stash específico cuando ya no lo necesitas
- `clear all stashes`- Elimina todos los stashes de una vez
- `git stash branch`- Crea un nuevo branch y le aplica un stash.

Es importante que el mensaje del stash deje claro qué se está probando haciendo uso del mismo.

## Historial de git
[Link a la referencia](https://www.w3schools.com/git/git_history.asp?remote=github)

Git por defecto guarda un registro de cada cambio en el repositorio. Se pueden utilizar comandos para ver qué y quién ha realizado cambios en el repositorio. 

- `git log` - Enseña todos los commits realizados
	- (utilizando `/` seguido de la búsqueda y luego presionando enter se puede hacer una búsqueda de los commits, `n` se puede utilizar para buscar la siguiente coincidencia. Para salir se puede utiliza q) 
- `git log --oneline` - Enseña un resumen de los commits con su hash en una línea
- `git log --author="Alice"`- Busca commits realizados por un autor
- `git log --since="2 weeks ago"`
- `git log --since="2 weeks ago"` -Muestra únicamente los commits que se han realizado desde hace 2 semanas
- `git log --stat` - Muestra qué archivos han sido cambiados en cada commit y cuantas líneas se han añdadido o borrado
- `git log --graph` - Muestra un gráfico simple con el historial de la rama con la que se está trabajando.

- `git show <commit>` - Muestra todos los detalles de un commit específico
- `git diff` - Muestra los commits que no se han establecido
- `git diff --staged` - Enseña los cambios establecidos en el commit
- `git diff <commit1> <commit2>` - Compara 2 commits

## Ayuda en git
[Link a la referencia](https://www.w3schools.com/git/git_help.asp?remote=github)

En este apartado se describen los comandos de ayuda para Git.

- `git help <command>` - Enseña la página de manual para un comando
- `git <command> --help` - Misma que el comando previo
- `git <command> -h` - Resumen rápido de opciones
- `git help --all` - Genera una lista de todos lo comandos posbles
- `git help -g` - List guides and concepts

## Branch (Rama)
[Link a la referencia](https://www.w3schools.com/git/git_branch.asp?remote=github)

En git, una rama es similar a la generación de un workspace paralelo en el que se pueden probar diferentes ideas para un mismo código. Normalmente se usa para arreglar bugs, desarrollo de herramientas y experimentación. (*La existencia de esto es la razón por la que pienso que el stash no es tan útil*). Al acabar los cambios de la rama se puede hacer un Merge que permite añadir todo a la rama principal.

Este apartado es MUY IMPORTANTE, así que, para comprobar que todo lo que se ha aprendido previamente. Para ello se propone una práctica:

Primero se genera un documento dentro del workspace en el que se está trabajando:

```sh title:"Se crea un archivo y se edita"
cd workspace
touch prueba.txt
nano prueba.txt
```

Se añade el texto previsto y se hace `ctrl+x`e `y` para guardar y salir. Ahora entrando en terreno de git:

```sh title:"add+commit"
git add prueba.txt
git commmit prueba.txt 
```

Se guarda y cierra el editor de texto y ya está listo.

**Crear un branch:** 

```sh: title:"Creacion de rama"
git branch rama_prueba
git branch
```

El segundo comando muestra todas las ramas de repositorio, mostrará  la maestra y la nueva. La `*` al lado de las ramas indica la posición en la que se está trabajando. Para moverse de la rama que se está utilizando a la nueva se utiliza el comando `checkout`.

```sh title:"Cambio de rama"
git checkout rama_prueba
git branch
```

Desde este momento los cambios no afectan a la rama principal y se muestra el `*`
en la nueva rama. En este momento se hace cambios sobre el txt generado con nano u otra herramienta. Ahora se comprueba el estado del git:

>[!tip] Cambio directo a la rama desde la creación
>Se puede cambiar directamente a la rama que se ha generado con el comando `-b`
>```sh title:ejemplo
>git branch -b rama_prueba
>```

```sh 
git status
```

Se muestran todos los cambios realizados en el Git. Por último se realiza un commit a la rama:

```sh
git commit -m "Se han anyadido x cambios"
```

Se utiliza `-d` para eliminar las ramas:

```sh
git branch -d rama_prueba
```

##### Listado de comandos:
- `git branch -name`- Crear la rama
- `git branch -m old-name new-name` - Renombrar una rama
-  `git branch`- Listar todas las ramas
-  `git checkout branch-name` or `git switch branch-name` -Cambiar de rama de trabajo
-  `git branch -D branch-name` - Forzar eliminado de una rama
- `git status` - Muestra la rama en la que te encuentras con sus cambios

## Merge (Unir)
[Link a la referencia](https://www.w3schools.com/git/git_security_ssh.asp?remote=github)
Este apartado parte del anterior [Branch(Rama)]. 

Hacer un Merge (o Unir) significa combinar cambios de una rama a otra. Así es como el trabajo se une tras trabajar por un tiempo en otra rama.  

Normalmente se cambia primero a la rama en la cual quieres unir tus cambios de la rama secundaria, luego se lanza el comando de Merge con el nombre de la rama secundaria cuyos cambios se quieren unir.

```sh
git checkout master
git merge rama_prueba
```

- **Siempre se debe realizar un commit o stash de manera previa al merge**. 
- **Es conveniente ir haciendo merge de la rama principal para evitar conflictos**
- 
>[!tip] Commit + Merge
> ```sh
 git merge --no-ff prueba.txt````


