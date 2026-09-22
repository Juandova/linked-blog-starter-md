
> [!info] Puedes transferir repositorios a otros usuarios o cuentas de organización.

https://docs.github.com/es/repositories/creating-and-managing-repositories/transferring-a-repository

## Acerca de las transferencias de repositorios

Al transferir un repositorio a un nuevo propietario, pueden administrar inmediatamente el contenido, los problemas, las solicitudes de incorporación de cambios, las versiones, proyectosy la configuración. También puedes cambiar el nombre del repositorio al transferir uno. Consulta [Renombrar un repositorio](https://docs.github.com/es/repositories/creating-and-managing-repositories/renaming-a-repository).

Los prerrequisitos para las transferencias de repositorio son:

* Al transferir un repositorio que posee a otra cuenta personal, el nuevo propietario recibirá un correo electrónico de confirmación. El correo electrónico de confirmación incluye instrucciones para aceptar la transferencia. Si el nuevo propietario no acepta la transferencia en un día, la invitación expirará.
* Para transferir un repositorio, debe tener acceso de administrador al repositorio.
* Los repositorios de GitHub.com solo se pueden transferir a otros propietarios en GitHub.com.
* Para transferirle un repositorio que te pertenece a una organización, debes tener permiso para crear un repositorio en la organización de destino.
* La cuenta objetivo no debe tener un repositorio con el mismo nombre o una bifurcación en la misma red.
* El propietario original del repositorio se agrega como colaborador en el repositorio transferido. El resto de los colaboradores del repositorio transferido permanecerá intacto.
* No se pueden transferir repositorios individuales derivados de una red de origen privada.

Si transfiere un repositorio privado a una GitHub Free cuenta de usuario u organización, el repositorio perderá el acceso a características como ramas protegidas y GitHub Pages. Consulte [planes de GitHub](https://docs.github.com/es/get-started/learning-about-github/githubs-plans).

Si el repositorio transferido contiene una acción enumerada en GitHub Marketplace, o tenía más de 100 clones o más de 100 usos de GitHub Actions en la semana anterior a la transferencia, GitHub retira permanentemente el nombre de propietario y la combinación de nombre del repositorio (`OWNER/REPOSITORY-NAME`) al transferir el repositorio. Si intenta crear un repositorio mediante una combinación de nombre de propietario retirado y nombre de repositorio, verá el error: "El repositorio `REPOSITORY_NAME` se ha retirado y no se puede reutilizar".

### ¿Qué se transfiere con un repositorio?

Cuando transfieres un repositorio, también se transfieren sus propuestas, solicitudes de extracción, wiki, estrellas y observadores. Si el repositorio transferido contiene webhooks, servicios, secretos, o llaves de implementación, estos permanecerán asociados después de que se complete la transferencia. Se conserva la información de Git acerca de las confirmaciones, incluidas las contribuciones. Además:

* Si el repositorio transferido es una bifurcación, sigue asociado con el repositorio ascendente.
* Si el repositorio transferido tiene alguna bifurcación, esas bifurcaciones seguirán asociadas al repositorio después de que se complete la transferencia.
* Si el repositorio transferido usa Almacenamiento de archivos de gran tamaño de Git, todos los Git LFS objetos se mueven automáticamente. Esta transferencia se produce en segundo plano, por lo que si tiene un gran número de Git LFS objetos o si los Git LFS propios objetos son grandes, puede tardar algún tiempo en producirse la transferencia.
* Cuando se transfiere un repositorio entre dos cuentas personales, las asignaciones de incidencias se dejan intactas. Cuando transfieres un repositorio desde una cuenta personal a una organización, las incidencias asignadas a los miembros de la organización permanecen intactas y todos los demás asignatarios de incidencias se eliminan. Solo los propietarios de la organización están autorizados a crear asignaciones de propuestas nuevas. Al transferir un repositorio de una organización a una cuenta personal, solo se conservan las incidencias asignadas al propietario del repositorio y se elimina cualquier otro usuario asignado a incidencias.
* Al transferir un repositorio de una organización a otra organización, los tipos de incidencias se dejan intactos si la nueva organización tiene un tipo de incidencia coincidente, y todos los demás tipos de incidencias se eliminan de las incidencias.
* Cuando transfieres un repositorio de una organización a una cuenta personal, se eliminan todos los tipos de incidencias de las incidencias.
* Si el repositorio transferido contiene un GitHub Pagessitio, los enlaces al repositorio de Git en la web y a través de la actividad de Git se redirigen. Sin embargo, no redirigimos GitHub Pages asociado con el repositorio.
* Todos los enlaces a la ubicación anterior del repositorio se redirigen de manera automática hacia la ubicación nueva. Al usar `git clone`, `git fetch` o `git push` en un repositorio transferido, estos comandos le redirigirán a la nueva ubicación o dirección URL del repositorio. Sin embargo, para evitar confusiones, es altamente recomendable actualizar cualquier clon local existente para que apunte a la nueva URL del repositorio. Puede hacerlo con `git remote` en la línea de comandos:

  ```shell
  git remote set-url origin NEW_URL
  ```

  > [!WARNING]
  > Si creas un nuevo repositorio o bifurcación en la ubicación anterior del repositorio, las redirecciones al repositorio transferido se eliminarán de forma permanente.
* Cuando transfieres un repositorio desde una organización a una cuenta personal, los colaboradores con permisos de solo lectura no se transferirán. Esto es porque los colaboradores no pueden tener acceso de solo lectura a los repositorios que pertenecen a una cuenta personal. Para obtener más información sobre los niveles de permisos de repositorio, consulte [Niveles de permisos para un repositorio de una cuenta personal](/es/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/permission-levels-for-a-personal-account-repository) y [Roles de repositorio para una organización](/es/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization).
* Los patrocinadores que tengan acceso al repositorio a través de un nivel de patrocinio podrían verse afectados. Consulte [Administrar tus niveles de patrocinio](/es/sponsors/receiving-sponsorships-through-github-sponsors/managing-your-sponsorship-tiers#adding-a-repository-to-a-sponsorship-tier).
* Los paquetes asociados al repositorio se pueden transferir o pueden perder su vínculo al repositorio, en función del registro al que pertenecen. Consulta [Acerca de los permisos para los Paquetes de GitHub](/es/packages/learn-github-packages/about-permissions-for-github-packages#about-repository-transfers).

Consulta [Administrar repositorios remotos](/es/get-started/git-basics/managing-remote-repositories).

### Transferencias de repositorios y organizaciones

Para transferir repositorios a una organización, debes tener permiso para crear repositorios en la organización receptora y para transferir repositorios fuera de la organización de origen. Es posible que el propietario de una organización o empresa haya establecido una directiva que impida que determinados usuarios realicen estas acciones.

Una vez que se transfiere un repositorio a una organización, los parámetros de permiso del repositorio de la organización predeterminados y los privilegios de membresía predeterminados se aplicarán al repositorio transferido.

## Transferir un repositorio que pertenece a tu cuenta personal

Puedes transferir tu repositorio a cualquier cuenta personal que acepte la transferencia de tu repositorio. Cuando se transfiere un repositorio entre dos cuentas personales, el propietario del repositorio original y los colaboradores se agregan automáticamente como colaboradores al repositorio nuevo.

Si publicó un GitHub Pages sitio en un repositorio privado y agregó un dominio personalizado, antes de transferir el repositorio, es posible que desee quitar o actualizar los registros DNS para evitar el riesgo de una adquisición de dominio. Consulte [Administración de un dominio personalizado para el sitio de GitHub Pages](/es/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

1. En GitHub, navegue hasta la página principal del repositorio.
2. Debajo del nombre del repositorio, haz clic en **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Si no puedes ver la pestaña "Configuración", selecciona el menú desplegable **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** y, a continuación, haz clic en **Configuración**.

   ![Captura de pantalla de un encabezado de repositorio en el que se muestran las pestañas. La pestaña "Configuración" está resaltada con un contorno naranja oscuro.](/assets/images/help/repository/repo-actions-settings.png)
3. En la parte inferior de la página, en la sección "Zona de peligro", haz clic en **Transferir**.
4. Lea la información sobre cómo transferir un repositorio y, a continuación, en "Nuevo propietario", elija cómo especificar el nuevo propietario.
   * Para elegir una de las organizaciones, seleccione **Seleccionar una de mis organizaciones**.

     * Seleccione el menú desplegable y haga clic en una organización.
     * Opcionalmente, en el campo "Nombre del repositorio", escriba un nuevo nombre para el repositorio.

> [!NOTE]
> Tienes que ser propietario de la organización de destino para poder cambiar el nombre del repositorio.

   * Para especificar una organización o un nombre de usuario, seleccione **Especificar una organización o nombre de usuario** y, después, escriba el nombre de usuario de la organización o del nuevo propietario.
5. Lee las advertencias acerca de la posible pérdida de características en función de la suscripción de GitHub del propietario nuevo.
6. Después de **Escribir REPOSITORY NAME para confirmar**, escriba el nombre del repositorio que quiere transferir y haga clic en **Lo entiendo, quiero transferir este repositorio**.

## Transferir un repositorio que le pertenece a tu organización

Si tienes permisos de propietario en una organización o permisos de administrador para uno de sus repositorios, puedes transferir un repositorio que le pertenece a tu organización a tu cuenta personal o a otra organización.

1. Inicia sesión en tu cuenta personal que tiene permisos de administrador o propietario en la organización a la que le pertenece el repositorio.
2. En GitHub, navegue hasta la página principal del repositorio.
3. Debajo del nombre del repositorio, haz clic en **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Si no puedes ver la pestaña "Configuración", selecciona el menú desplegable **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** y, a continuación, haz clic en **Configuración**.

   ![Captura de pantalla de un encabezado de repositorio en el que se muestran las pestañas. La pestaña "Configuración" está resaltada con un contorno naranja oscuro.](/assets/images/help/repository/repo-actions-settings.png)
4. En la parte inferior de la página, en la sección "Zona de peligro", haz clic en **Transferir**.
5. Lea la información sobre cómo transferir un repositorio y, a continuación, en "Nuevo propietario", elija cómo especificar el nuevo propietario.
   * Para elegir una de las organizaciones, seleccione **Seleccionar una de mis organizaciones**.

     * Seleccione el menú desplegable y haga clic en una organización.
     * Opcionalmente, en el campo "Nombre del repositorio", escriba un nuevo nombre para el repositorio.

> [!note]
> Tienes que ser propietario de la organización de destino para poder cambiar el nombre del repositorio.

   * Para especificar una organización o un nombre de usuario, seleccione **Especificar una organización o nombre de usuario** y, después, escriba el nombre de usuario de la organización o del nuevo propietario.
6. Lee las advertencias acerca de la posible pérdida de características en función de la suscripción de GitHub del propietario nuevo.
7. Después de **Escribir REPOSITORY NAME para confirmar**, escriba el nombre del repositorio que quiere transferir y haga clic en **Lo entiendo, quiero transferir este repositorio**.