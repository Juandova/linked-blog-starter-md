Para la creación de toda la documentación se ha hecho uso de los tutoriales de la web[W3School](https://www.w3schools.com/git/#) y la [ documentación oficial de Git](https://git-scm.com/docs).

*¿Qué es?*
Es un sistema de control de versiones
## Introducción
Este documento describe parámetros clave y definiciones sin entrar al uso oficial de Git. En caso de ya conocer los términos se recomienda saltar al documento [[Git Básico]]
##### Conceptos clave:
- *Repositorio*: Una carpeta en la que git sigue tu proyecto e historia del mismo
- *Clon*: Es una copia de un repositorio remoto en tu máquina
- *Stage*: Decirle a Git qué quieres guardar a continuación
- *Commit*: Hacer un guardado instantáneo de los cambios establecidos
- *Branch*: Trabajar en distintas versiones, o características al mismo tiempo
- *Merge*: Combinar cambios de diferentes "Branches"
- *Pull*: Obtener los útimos cambios de un repositorio remoto
- *Push*: Mandar tus cambios a un repositorio remoto
##### Pasos para trabajar con Git:
1. Inicializar Git en una carpeta conviertiendola en un repositorio
2. Git crea una carpeta oculta para seguir los cambios de dicha carpeta
3. Cuando un fichero se cambia, añade o borra se considera que se ha modificado
4. El usuario selecciona los archivos que desea guardar con *Stage*
5. Los archivos que han pasado por *Stage* han realizado un *Commit*, que lee da a Git la orden de guardar de manera permanente un guardado instantáneo de los archivos en *Stage*
6. Git te permite ver el historial de cada commit
7. Puedes revertir a cualquier commit previo
8. **Git no guarda una copia separada de cada archivo cada vez que se realiza un commit, pero sigue el flujo de cambios que se han realizado en cada commit**
##### Elemental: Diferencia con Github
- **$\neq$ Github, no son lo mismo** 
- Github es una herramienta que utiliza Git
- Github es el host más grande de código del mundo

Para instalar Github en distintos sistemas operativos:

- [ ]  A completar luego para el resto de dispositivos

En el caso de Linux, para la imagen de  Ubuntu suele venir pre instalado, para hacer una instalación prueba:

```sh title:"Codigo instalacion git"
sudo apt-get install git
```

Para comprobar la version  o ver que ha sido correctamente instalado utilizar:

```sh title:"Codigo comprobacion git"
git --version
```

>[!missing] En caso de que no funcione:
> Leer [[Variables de Entorno]]

##### ¿Problemas con la instalación?
[Lee este link](https://www.w3schools.com/git/git_install.asp?remote=github#:~:text=Troubleshooting%20Git%20Installation)

##### Editor de código/texto por defecto

Se puede establecer un editor de código como el VS Code (el más utilizado para edición de código) para que funcione por defecto con Git:

```sh title:"VSCode por defecto git"
git config --global core.editor "code --wait"
```


> [!warning] 
> En caso de no querer usar VS Code, se puede utilizar el blo de notas por ejemplo 
> ```sh title:"Bloc de notas por defecto"
> git config --global core.editor "notepad"
> ```


##### Variable de  Entorno PATH
Añadir Git al PATH de variables de entorno significa que podrás utilizar los comandos de Git en cualquier ventana de terminal abierta.

Saltarse este paso significa que solo serás capaz de usar el Git en Git Bash, en el caso de Windows o Terminal, en el caso de macOS y Linux.

Explicación más detallada de las variables de entorno en [[Variables de Entorno]]

##### Finales de línea (Line Endings)
Git puede convertir los finales de línea en archivos de texto.

En Windows, normalmente es recomendable seleccionar **"Checkout Windows-style, commit Unix-style line endings"** (extraer archivos con finales de línea de estilo Windows y confirmar cambios con finales de línea de estilo Unix).

Esto ayuda a evitar problemas al compartir código con personas que utilizan distintos sistemas operativos.

Los **finales de línea** son los caracteres especiales que indican dónde termina una línea de texto y comienza la siguiente dentro de un archivo.

Los distintos sistemas operativos han utilizado históricamente diferentes convenciones:

- **Windows**: usa dos caracteres, **CR + LF** (`\r\n`).
- **Linux** y **macOS moderno**: usan un único carácter, **LF** (`\n`).
- **macOS antiguo**: utilizaba **CR** (`\r`), aunque hoy en día prácticamente ya no se usa.

##### Actualizar o desinstalar Git:

**Actualizar (Update):** Descarga y ejecuta el instalador más reciente, o utiliza tu gestor de paquetes (por ejemplo, `brew upgrade git` o `sudo apt-get upgrade git`).
Es recomendable mantener Git actualizado para disponer de las últimas funcionalidades y correcciones de seguridad.

**Desinstalar (Uninstall):** Utiliza **"Agregar o quitar programas"** en Windows, o tu gestor de paquetes en Mac/Linux.

##### Configurar git
Es impotante que Git te reconozca como usuario, la configuración se puede modificar en cualquier momento. Para eso se aplica:

```sh
git config --global user.name "Your Name"
```

Y posteriormente el correo personal:

```sh
git config --global user.email "you@example.com"
```

Esta información se puede cambiar en cualquier momento pero Git recordará los commits previos manteniendo el usuario anterior.

Se puede usar `--global`para todos los repositorios del ordenador y `--local` para el repositorio actual.  

**Niveles de configuración:**
- **System** (Para todos los usuarios del equipo): `git config --system`
- **Global** (Para el usuario actual): `git config --global`
- **Local** (Repositorio actual): `git config --local`

##### Visualizar tu información
Se puede visualizar toda la información de git con el siguiente comando:

```sh
git config --list
```

Para cambiar cualquier variable sólo hay que volver a enviar el `git config`

Se utiliza el comando `unset` para eliminar un ajuste:

```shell
git config --global --unset code.editor
```

Para establecer una nueva rama por defecto para nuevos repositorios como `m̀ain` y `master`.

```shell
git config --global init.defaultBranch main
```

Ahora que ya está confgigurado se puede pasar a crear un repositorio.

>[!tldr] Siguientes pasos
$\hookrightarrow$ Para plantear un Vault compartido ver [[Vault compartido]]
$\hookrightarrow$ Para continuar comenzar con la creación de un repositorio ver [[Git Básico]].
