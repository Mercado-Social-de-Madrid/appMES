# Versiones

## v2.3.1
Julio 2025

### Errores corregidos

- HOTFIX: arreglado error en búsqueda si campo embedding está vacío


## v2.3
Julio 2025

### Novedades y cambios

- Añadida función para gestionar entidades y socias de intercooperación
- Añadido campo para el reverso del DNI en el formulario público de alta
- Ajustados los umbrales de la búsqueda semántica
- Documentación de administración actualizada
- Actualizadas las traducciones a euskera
- Se han desactivado los idiomas catalán y gallego ya que de momento no se usan

### Errores corregidos

- TG-81: borrado Madrid de la imagen de las chapas de fondo


## v2.2.1
Junio 2025

### Novedades y cambios

* Búsqueda semántica en catálogo de entidades en base a productos y servicios
* Añadida documentación y guía de usuarias de la aplicación
* Actualizadas las traducciones a euskera
* Endpoint de datos en formato GeoJSON para mapas incrustados

### Errores corregidos
* TG-109: Arreglo del valor del campo 'register_consumer_url' en la respuesta de la API
* TG-116: Elimina la red social si la url está vacía
* TG-118 - XFrameOptionsExempt en vista de catálogo
* TG-111 - Retoques gráficos y traducciones

## v2.2.0
Febrero 2025

### Novedades y cambios

* Landing page de inicio con información de la app y catálogo público de los mercados
* Formulario de alta de consumidora (para incrustar mediante iframe y en la app)
* Añadida funcionalidad para personalizar textos de la interfaz por cada mercado y su previsualización
* Añadido campo a las entidades de "Productos y servicios"
* Creados comandos de comprobación e importación de enlaces a infografía de balance

### Errores corregidos

* HA-242: Fix en codificación HTML para las notificaciones de ofertas en la app
* TG-88: Error en redirección tras crear usuaria sin ser admin de mercado
* TG-89: Mostrar en el filtrado de categorías solo las relativas a ese mercado concreto
* TG-107: Corregido error en URL de web en el partial de redes sociales
* TG-103: Error en imágenes de plantilla de email

## v2.1.0
Agosto 2024

### Novedades y cambios

* Añadido soporte multi-idioma configurable por mercado
* Añadidas traducciones de interfaz a euskera
* Añadido dashboard para admin
* Integración con Herramienta Gestora con DRF

### Errores corregidos

* MES-165: Arreglo de renderizado de PDF de carnet


## v2.0.0
Mayo 2024

### Novedades y cambios

* Re-escritura completa del código antiguo del servidor de la app para gestión multi-mercado
* Configuración y permisos específicos de usuarios por mercado social
* Añadido modelo para definir de forma dinámica las redes sociales del formulario
* Añadido comando para generar y comprobar posibles números de socia duplicados
* Integración con Herramienta Gestora con DRF


Para consultar el histórico de versiones y los cambios incluídos en cada version puedes verlo en la [página de releases de Github](https://github.com/Mercado-Social-de-Madrid/appMES/releases){ target=blank }.
