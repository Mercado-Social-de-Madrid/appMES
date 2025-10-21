---
icon: material/web-plus
---

# Web

Son vistas ya preparadas para mostrarse en la web, ya sea la web original en el dominio `mercadosocial.app` o como parte
de otra web. Un caso práctico puede ser añadir estas vistas dentro de la web de un Mercado territorial concreto. 

/// admonition | Código de mercado
    type: info
En los siguientes puntos, el texto `{codigo_de_mercado}` hay que sustituirlo por el nuestro. Éste se puede ver debajo 
del nombre de nuestro territorio en la esquina superior izquierda. Suele ser una abreviación de 3 letras.
///


## Qué vistas se pueden integrar

### 1. :material-format-list-text: Listado de entidades

![Web listado entidades](../../assets/images/web-listado-entidades.png){ loading=lazy }

Se muestra el listado de nuestras entidades activas. Al pulsar el botón "Más información de la entidad" se abre un pop-up
con la descripción, productos/servicios y dirección.

Si la entidad tiene añadido un link a su infografía de balance/auditoría social, se muestra el sello configurado en la pantalla 
[Personalizar mercado](../../menu_lateral/personalizacion/#1-datos-basicos). Al pulsar dicha imagen se abre en otra pestaña su infografía.

De la misma manera, si hay información de :material-leaf: ventajas, aparece un botón que muestra su información.

A esta web se accede a través de la url: 
```
https://mercadosocial.app/d/{codigo_de_mercado}
```

### 2. :material-form-textbox: Formulario de alta de consumidoras

Para los territorios que tengan registro de socias consumidoras, se ofrece un formulario público para facilitar la
solicitud de alta por parte de personas interesadas.

![Formulario alta consumidora](../../assets/images/formulario-alta-consumidora.png){ loading=lazy }

Esta es la dirección del formulario de registro:
``` 
https://mercadosocial.app/consumer_register/{codigo_de_mercado}
```

Más detalles del funcionamiento de este formulario en la sección [Consumidoras](../../menu_lateral/consumidoras/#2-solicitud-mediante-formulario-publico)

/// admonition | Habilitar registro de consumidoras
    type: info
Por defecto este registro no está habilitado, si se quiere activar, hay que avisar al equipo de desarrollo.
///


## Cómo realizar la integración

1. Mediante enlace directo, usando las direcciones anteriores en un enlace web dentro de otra página
2. Insertar estas vistas dentro de otra web mediante el elemento `iframe`. 
Para ello habría que hablar con la persona administradora del sitio web del Mercado correspondiente, se usa un código 
parecido a este: 
```
 <iframe src="{enlace}" title="{titulo}" ...></iframe> 
```
