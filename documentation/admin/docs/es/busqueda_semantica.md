---
icon: material/comment-search-outline
---

# Búsqueda semántica

Esta función mejora notablemente los resultados de búsquedas de usuarias ya que no solo realiza búsquedas por palabras exactas 
si no que permite encontrar entidades por
aproximaciones de significado de las palabras descritas en el campo "Productos y servicios", por ejemplo si una zapatería
ha puesto la palabra "Zapatos" entre sus productos y un usuario busca palabras similares como "zapatillas" o "calzado", 
esta zapatería aparecerá en la lista de resultados, posicionada por orden según su aproximación semántica y con un 
indicador de esa proximidad. En el modelo anterior de búsqueda por palabras exactas, esta entidad no aparecería entre los
resultados al no haber una coincidencia completa de palabras.

/// admonition | Explicación técnica
    type: info
Esta "magia" es posible gracias a lo que se conoce técnicamente como [modelos de embeding](https://es.wikipedia.org/wiki/Word_embedding){ target=blank }
, que en resumen transforman palabras a números (este proceso se llama vectorización) que representan su posición semántica en un 
espacio multidimensional y permiten calcular la "distancia" o similitud frente a otras palabras.
///


Esta búsqueda por similitud semántica no excluye la búsqueda anterior por palabras exactas si no que se hace una combinación 
según este algoritmo:

- Búsqueda por palabras exactas en los campos de entidad: nombre, descripción corta, descripción completa y productos/servicios
- Búsqueda por similitud semántica
- Los resultados se ordenan mostrando las coincidencias por palabras exactas en primer lugar, seguido de los resultados por 
similitud semántica ordenados por dicha similitud. 
- En ambos casos se muestra una vista que indica si el resultado viene de búsqueda exacta o su proximidad semántica.
