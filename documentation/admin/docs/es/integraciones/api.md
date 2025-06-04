---
icon: material/api
---

# API

Un API es una interfaz de comunicación con la base de datos del servidor que permite acceder a los datos en bruto y 
estructurados en formato Json de la aplicación del MES para utilizarse en aplicaciones externas. 

Un caso de uso habitual es una web que quiera mostrar los datos con un estilo personalizado.

/// admonition | Web de Aragón
    type: info
La página web del Mercado de Aragón utiliza este API para mostrar la información de entidades organizadas primero por 
categorías con iconos personalizados. [Pulsando aquí](https://mercadosocialaragon.net/catalogo-entidades/){ target=blank }
se puede ver el catálogo de entidades según lo han diseñado desde su mercado.
///

Esta es la URL base del API `https://mercadosocial.app/api/v2/` y ahora mismo permite acceder a los siguientes modelos de datos:

- Lista de mercados: `nodes/`

Por cada mercado usaremos la URL base `https://mercadosocial.app/api/v2/nodes{id_nodo}/` 
(sustituyendo `{id_nodo}` por el id numérico correspondiente) y podremos acceder a estos datos:

- Categorías: `categories/`
- Proveedoras: `providers/`
- Noticias: `news/`
- Ventajas: `benefits/`
- Ofertas: `offers/`
- Geolocalización de proveedoras: `providers_geojson/` (este servicio se usa para localizar las entidades en los mapas uMap
según se describe en la sección [Mapa](mapa.md))

/// admonition | Otros servicios
    type: note
Existen algunos servicios más en este API relacionados con autenticación de usuarios, actualización de perfiles y creación
de registros de socias (entidades o consumidoras). Está pendiente crear una documentación técnica para el API más completa, 
pero si hicieran falta para alguna integración, consultar al equipo técnico.
///