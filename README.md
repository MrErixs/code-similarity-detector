# Model Code Similarity Detector

## Objetivo del proyecto
El objetivo general es construir un modelo que reciba dos códigos fuente y determine que tan similares son.
En nuestro caso, como el dataset AI-SOCO está organizado por autores, la similitud inicial se define de la siguiente manera:
`label = 1`: los dos códigos fueron escritos por el mismo autor.
`label = 0`: los dos códigos fueron escritos por autores diferentes.

## Dataset utilizado
El dataset utilizado es AI-SOCO.
AI-SOCO contiene códigos fuente escritos en C++ y está organizado con archivos CSV que relacionan:
`uid`: identificador del autor.
`pid`: identificador del archivo de código.

## Generación de pares

El dataset AI-SOCO originalmente no está construido como un problema de comparación entre dos códigos, sino como un problema de identificación de autoría. Es decir, cada archivo de código está relacionado con un autor mediante las columnas `uid` y `pid`.

Por esta razón, antes de entrenar un modelo de similitud fue necesario adaptar el dataset a un formato de pares de códigos. Para lograrlo, generamos un nuevo archivo llamado `pairs.csv`, donde cada fila contiene dos códigos fuente y una etiqueta binaria que indica si se consideran similares o no.

La lógica utilizada fue la siguiente:

- Si dos códigos pertenecen al mismo autor (`uid1 == uid2`), se genera un par positivo con `label = 1`.
- Si dos códigos pertenecen a autores diferentes (`uid1 != uid2`), se genera un par negativo con `label = 0`.

De esta forma, la similitud se interpreta inicialmente como similitud de estilo de programación asociada al autor. Es decir, el modelo no busca todavía comprobar si dos códigos resuelven exactamente el mismo problema, sino identificar patrones de similitud entre códigos escritos por la misma persona.

Donde:
- pid1: identificador del primer código.
- pid2: identificador del segundo código.
- uid1: autor del primer código.
- uid2: autor del segundo código.
- label: etiqueta de similitud.
- path1: ruta local del primer archivo de código.
- path2: ruta local del segundo archivo de código.

## Preprocesamiento del código
Después de generar los pares de códigos, el siguiente paso fue preparar cada archivo fuente para poder compararlo de forma más adecuada.

No conviene comparar los códigos directamente como texto plano, ya que dos programas pueden ser muy similares aunque tengan diferencias superficiales como espacios, saltos de línea, comentarios, nombres de variables o valores numéricos específicos.

Aunque el texto no es exactamente igual, ambos siguen una estructura similar. Por esta razón, se implementó un preprocesamiento basado en tokenización y normalización.

Preprocesamiento:
- Lee el archivo de código fuente usando su ruta.
- Elimina comentarios de una línea (//) y comentarios de varias líneas (/* ... */).
- Divide el código en tokens, es decir, en unidades pequeñas como palabras reservadas, identificadores, números, operadores y símbolos.
- Normaliza los tokens para reducir diferencias superficiales entre programas.

Normalización:
- Las palabras reservadas de C++ se conservan, pero se pasan a mayúsculas.
- Los nombres de variables, funciones u otros identificadores se reemplazan por ID.
- Los valores numéricos se reemplazan por NUMBER.
- Los operadores y símbolos se conservan tal como aparecen.

# Proximos paos
Después del preprocesamiento, el siguiente paso será realizar la extracción de características, también conocidas como features. Estas características serán valores numéricos que representen qué tan parecidos son dos códigos después de haber sido convertidos a tokens normalizados.

### Extracción de features

La idea general será transformar cada par de códigos en un conjunto de métricas de similitud:

Código 1 → tokens normalizados
Código 2 → tokens normalizados
Tokens del código 1 + tokens del código 2 → métricas de similitud

De esta forma, en lugar de comparar directamente el texto original de los programas, se compararán sus representaciones tokenizadas. Esto permite reducir el impacto de diferencias superficiales como nombres de variables, valores numéricos o comentarios.

### Archivo esperado

El resultado de este paso será un nuevo archivo:

outputs/features.csv

Este archivo contendrá una fila por cada par de códigos. Cada fila tendrá las métricas calculadas y la etiqueta esperada.

Ejemplo de estructura:

pid1,pid2,jaccard,dice,length_difference,length_ratio,label
43096,60809,0.82,0.90,5,0.94,1
37014,28375,0.21,0.35,80,0.40,0

### Features propuestas

Para una primera versión se pueden calcular las siguientes métricas:

#### Jaccard similarity
Mide cuántos tokens comparten ambos códigos en relación con el total de tokens únicos. Un valor cercano a 1 indica mayor similitud.

#### Dice similarity
Mide la similitud entre los conjuntos de tokens, dando más peso a los tokens compartidos. También toma valores entre 0 y 1.

#### Length difference
Mide la diferencia absoluta entre la cantidad de tokens de ambos códigos.

Ejemplo:

Código 1: 100 tokens
Código 2: 80 tokens
length_difference = 20

#### Length ratio
Compara el tamaño del código más pequeño contra el tamaño del código más grande.

Ejemplo:

Código 1: 100 tokens
Código 2: 80 tokens
length_ratio = 0.8

### Entrenamiento del modelo

Una vez generado features.csv, el siguiente paso será entrenar un modelo de Machine Learning para clasificar los pares de códigos.

El modelo recibirá como entrada las features calculadas y aprenderá a predecir la etiqueta:

- 1 = códigos similares
- 0 = códigos no similares

Algunos modelos candidatos para esta primera versión son:

- Random Forest
- Logistic Regression
- KNN
- Decision Tree

Para iniciar, Random Forest puede ser una buena opción porque funciona bien con datos tabulares y permite entrenar un primer modelo de forma rápida.

### Evaluación

Finalmente, el desempeño del modelo se evaluará usando métricas de clasificación binaria:

- Accuracy
- Precision
- Recall
- F1-score
- Matriz de confusión

Estas métricas permitirán analizar qué tan bien el modelo logra diferenciar entre códigos considerados similares y no similares.

### Relación con el artículo base

Este enfoque sigue la idea general del artículo base, donde primero se tokenizan los códigos, después se calculan medidas de similitud entre las secuencias de tokens y finalmente se usa un modelo de Machine Learning para clasificar los pares.