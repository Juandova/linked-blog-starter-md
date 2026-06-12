Las **variables de entorno** son pares **nombre = valor** que el sistema operativo pone a disposición de los programas mientras se ejecutan.

Sirven para almacenar configuración sin tener que escribirla directamente en el código.

### Ejemplos comunes

- `PATH`: indica dónde buscar programas ejecutables.
- `HOME`: carpeta personal del usuario.
- `LANG`: configuración de idioma.
- `PORT`: puerto donde debe escuchar una aplicación.
- `API_KEY`: clave para acceder a una API.

> [!example] Ejemplo
> Imagina que tienes:
> ```sh
> API_KEY=abc123
> PORT=3000
> ```
> En caso de un programa de python se guardaría como un valor de entorno que se puede leer como:
> ```Python
> import os
api_key = os.getenv("API_KEY")
puerto = os.getenv("PORT")
> ```
> 

En Linux se definen como:
```sh
export PORT=3000
```

Y para verla:
```sh
echo $PORT
```

[Link a la instalacion](https://www.w3schools.com/git/git_install.asp?remote=github#:~:text=PATH%20Environment)
