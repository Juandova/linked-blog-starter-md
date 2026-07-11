---
tags:
  - MASTER/MUSANTTA/Practicas
  - programación
date: 2026-07-09
---
> [!summary]  Plugin de [[Visual Stucio Code]]
> Que detecta automáticamente etiquetas como las de [[Notas IDE]] y genera una lista de tareas pendientes, la cual muestra en un panel lateral

- [TODO Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)

---
## Instalación

En extensiones de Visual Studio Code, buscar `todo tree` de Gruntfuggly, e instalar.

##### Dependencia `ripgrep`

```sh
sudo apt install ripgrep
```

Comprobar la instalación:

```sh
which rg
```

Resultado esperado:

```
/usr/bin/rg
```

---

### Problema encontrado

Tras instalar la extensión aparecía el error:

```
Todo-Tree: Failed to find vscode-ripgrep - please install ripgrep manually and set 'todo-tree.ripgrep' to point to the executable
```

Aunque `ripgrep` estaba correctamente instalado, la extensión no era capaz de localizar el ejecutable automáticamente.

---
#### Solución

Editar la configuración de usuario de VS Code:

```
Ctrl + Shift + P
Preferences: Open User Settings (JSON)
```

Añadir:

```json
{
    "todo-tree.ripgrep": "/usr/bin/rg"
}
```

Guardar y ejecutar:

```
Developer: Reload Window
```

---
## Configuración

- Por defecto, Todo Tree detecta principalmente `TODO`, `FIXME`, `BUG` y `HACK`.
- Es posible añadir etiquetas personalizadas mediante la opción:

### Opción 1.  Mediante la configuración del pluglin

CRTL + SHT + X -> extensión Todo Tree -> Manage -> Settings 

buscar Todo-tree > General: tags y agregar las etiquetas: OPTIMIZE, DEPRECATED, REVIEW
![[configuración_tags_todo_tree.png]]
###  Opción 2. Editando el archivo .json

```json
"todo-tree.general.tags": [
    "TODO",
    "FIXME",
    "REVIEW",
    "NOTE",
    "WARNING",
    "HACK",
    "OPTIMIZE",
    "DEPRECATED"
]
```

Esto permite mantener un seguimiento mucho más organizado de la deuda técnica del proyecto.

