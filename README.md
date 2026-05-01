# Detección de Código generado por IA vs Código Humano (Lenguaje C++)

## Objetivo del proyecto
Desarrollar y evaluar modelos de aprendizaje supervisado capaces de clasificar fragmentos de código C++ como generados por IA o escritos por humanos.

### Objetivos específicos:
* Preprocesar fragmentos de código C++ para reducir ruido y conservar patrones.
* Transformar el código a vectores numéricos usando TF-IDF.
* Entrenar y comparar modelos de clasificación binaria como Random Forest, XGBoost.
* Evaluar el desempeño mediante métricas de evaluación.
* Identificar limitaciones del modelo y posibles mejoras.

## Dataset utilizado
El dataset original analizado es [H_AIRosettaMP.csv](https://zenodo.org/records/13908858).

La exploración de este dataset se encuentra en un archivo en repositorio (Ruta: src >> eda >> analisis_csv.cpp).

Para la primer versión de modelos se seleccionaron los ejemplos no duplicados de códigos en C++. Etiquetando con 1 código generado por IA y con 0 código escrito por un humano. El detalle de este dataset está en un archivo en repositorio (Ruta: src >> eda >> analisis_cpp_csv.cpp). Este está desbalanceado aproximadamente en proporción 6:1 siendo mayor el código generado por IA.

Para la segunda y tercer versión de modelos se balanceó el dataset con ejemplos de códigos humanos del dataset [AI-SOCO](https://github.com/AliOsm/AI-SOCO).

## Versión 1: Dataset desbalanceado

**=> 1.1. Random Forest (class_weight="balanced")**

Ajusta automáticamente mayor peso a la clase minoritaria durante el entrenamiento.

**=> 1.2. XGBoost (scale_pos_weight)**

Incrementa la penalización si el modelo comente errores sobre la clase minoritaria.

**=> 1.3. Balanced Random Forest Classifier (imbalanced-learn)**

Aplica técnicas de submuestreo a la clase mayoritatia para equilibrar la distribución de clases al entrenar. Lo hace contando todos los ejemplos de la clase minoritaria y seleccionando aleatoriamente la misma cantidad de ejemplos de la clase mayoritaria. Este balanceo interno es para cada árbol, no se aplica permanentemente al dataset original.

## Versión 2: Dataset balanceado

**=> 2.1. Random Forest**

**=> 2.2. XGBoost**

## Versión 3: Dataset desbalanceado con CodeBERT

Transformer especializado en código fuente. Utiliza una arquitectura profunda de 12 capas y embeddings de 768 dimensiones, con una entrada máxima de 512 tokens. Aunque teóricamente captura mejor el contexto del código, en nuestras pruebas no superó el rendimiento de XGBoost balanceado y además requirió mayor costo computacional.

### Evaluación

Finalmente, el desempeño del modelo se evalua usando métricas de clasificación binaria:

- Accuracy
- Precision
- Recall
- F1-Score
- Matriz de confusión

Estas métricas permitirán analizar qué tan bien el modelo logra diferenciar entre códigos considerados similares y no similares.

**Métricas reportadas para el conjunto de test:**

![Evaluación de métricas en conjunto test](https://github.com/MrErixs/code-similarity-detector/blob/main/outputs/resumen_resultados.png)

## Referencias

1. S. Feng, W. Suo, Y. Wu, D. Zou, Y. Liu, and H. Jin. (2024, April) Machine Learning is All You Need: A Simple Token-based Approach for Effective Code Clone Detection. *ICSE ’24: IEEE/ACM 46th International Conference on Software Engineering, Art. no. 222*. doi: 10.1145/3597503.3639114.

2. Feng, Z., Guo, D., Tang, D., Duan, N., Feng, X., Gong, M., ... & Zhou, M. (2020, November). *Codebert: A pre-trained model for programming and natural languages. In Findings of the association for computational linguistics: EMNLP 2020 (pp. 1536-1547)*. doi: 10.18653/v1/2020.findings-emnlp.139
