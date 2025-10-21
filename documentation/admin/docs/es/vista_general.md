---
icon: material/image
---

# Vista general

## :material-calendar-clock: Un poco de historia

En 2018, el Mercado Social de Madrid desarrolló un proyecto para incentivar el consumo dentro de la
ESS a través de una moneda social y aplicaciones web y móviles (Software Libre) para gestionar este sistema y tener
información de las entidades y novedades del Mercado. 

En el año 2023 se dió de baja la moneda ya que no tuvo el impacto previsto, pero se aprovecharon el resto de funciones útiles
como el directorio y buscador de entidades y las notificaciones de novedades del Mercado y promociones de entidades, además
y se añadieron nuevas funciones para seguir fomentando el consumo dentro de la red: un carné de socia digital con el que
acceder a ventajas y descuentos que ofrezcan voluntariamente las entidades.

A principios de 2024, por iniciativa del Mercado de Aragón, se hizo una reestructuración muy grande del sistema para 
permitir añadir fácilmente nuevos mercados. Se reescribió completamente la aplicación web y el backend ya que se 
aprovechó para poner al día y quitar toda la deuda técnica que había ido quedando. Las aplicaciones móviles se actualizaron
para adaptarse al nuevo sistema multimercado.

A mediados de 2024 se añadió también un cambio importante por iniciativa de Navarra para permitir múltiples idiomas
en los textos de las apps y contenidos gestionados por el Mercado y entidades.

Desde entonces seguimos mejorando este sistema digital y también la coordinación entre territorios y equipo desarrollador.


## :material-flag-checkered: Objetivo 

El objetivo es facilitar las tareas de gestión de entidades de un Mercado, ayudar a las entidades de la ESS a promocionar sus servicios
y crear intercooperación, y ofrecer a las consumidoras una red que garantiza un consumo ético, fortaleciendo el vínculo 
al Mercado de estos tres perfiles mediante herramientas tecnológicas modernas y accesibles.


## :material-vector-square: Componentes del sistema

Aunque se le suela llamar de forma abreviada "La aplicación del MES", realmente este sistema se compone de 3 elementos
que se desarrollan de forma independiente:

- Aplicación web + Backend: Es la parte que funciona dentro de un servidor, gestiona la base de datos y permite acceder
a la web pública y paneles de gestión privados (administración, entidades y consumidoras). Además, proporciona la interfaz
de comunicación necesaria para las aplicaciones móviles (técnicamente conocida como [API](integraciones/api.md)).
La aplicación web se puede ver a través de la siguiente dirección: [mercadosocial.app](https://mercadosocial.app){ target=blank }.
Aqui se muestra una página de presentación y **enlaces a los listados de entidades de los diferentes territorios** incluidos en esta app.
- [Aplicación Android](https://play.google.com/store/apps/details?id=net.mercadosocial.moneda){ target=blank }: 
permite acceder a la información del mercado de forma rápida, integra notificaciones instantáneas
(como cuando llega un mensaje de Telegram o Whatsapp) para noticias del Mercado y ofertas de entidades y permite el acceso
de socias mediante usuario y contraseña para mostar su carné digital y ver sus ventajas. Esto último es configurable según 
el Mercado.
- [Aplicación iOS](https://apps.apple.com/es/app/mercado-social/id1458549528?itsct=apps_box_badge&itscg=30200){ target=blank }: 
para iPhone y iPad, con las mismas funciones que la de Android pero con algunos cambios de elementos visuales
para adaptarlos a los sistemas de iOS.

En este diagrama se muestra la infraestructura general
![Infraestructura de la app del MES](../assets/images/infraestructura-app-mes.jpg){ loading=lazy} 

## :material-keyboard-settings-outline: Características generales

Aunque se detalla su funcionamiento en las siguientes secciones, este es un resumen de las características del sistema:

- **Entidades proveedoras**: Listado de todas las entidades del mercado con su ficha de información y funciones de búsqueda 
en la web y las apps móviles
- **Carné digital**: Las socias pueden acceder a él con su usuario y contraseña a través de web y apps móviles. Las entidades
proveedoras, además pueden escanear el carné de una socia para comprobar su validez.
- **Noticias y ofertas**: para promoción de eventos del mercado y entidades. Se consultan desde la app y llegan con notificación de aviso.
- **Paneles de gestión** web según el perfil:
    - **Administración**: Para personas encargadas de la gestión de un mercado territorial. Permiten la gestión de socias
    (proveedoras y consumidoras) y toda la información pública que se ve en la web y apps móviles.
    - **Proveedoras**: pueden gestionar su información pública (descripción, servicios, rrss, imágenes...), publicar ofertas y 
    ver su carné digital
    - **Consumidoras**: pueden ver y descargar su carné digital, acceder a su información de socia, y ver las últimas noticias.

