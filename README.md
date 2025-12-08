# Sistema Clasificador de Etapas Procesales Laborales
## Tesis LexGO - Prototipo ML

Sistema híbrido que combina Machine Learning tradicional (TF-IDF + Random Forest) con generación de timelines para causas laborales de CABA/Buenos Aires.

---

## 📋 Requisitos Previos

### Python 3.8+

### Librerías necesarias:
```bash
pip install pypdf2 pandas scikit-learn matplotlib seaborn
```

---

## 🗂️ Estructura del Proyecto

```
lexgo-ml-tesis/
├── data/
│   ├── raw/                    # PDFs descargados (input)
│   ├── processed/              # Datasets procesados
│   └── sentencias_etiquetadas.csv  # Etiquetas manuales
├── models/
│   ├── vectorizer.pkl          # Modelo TF-IDF entrenado
│   └── clasificador.pkl        # Random Forest entrenado
├── results/
│   ├── confusion_matrix.png    # Visualización de resultados
│   ├── metricas.csv            # Métricas del modelo
│   └── *_analisis.json         # Resultados por PDF
└── scripts/
    ├── etiquetar_sentencias.py
    ├── preparar_datos.py
    ├── entrenar_clasificador.py
    ├── probar_clasificador.py
    └── sistema_integrado.py
```

---

## 🚀 Pipeline Completo (Paso a Paso)

### **FASE 1: Recolección y Etiquetado de Datos** (2-3 horas)

#### Paso 1.1: Descargar sentencias
- Ir a: https://www.cij.gov.ar/sentencias.html
- Buscar: "derecho laboral" en CABA
- Descargar 50 PDFs de sentencias laborales
- Guardar en: `data/raw/`

#### Paso 1.2: Etiquetar manualmente
```bash
python etiquetar_sentencias.py
```

**Categorías:**
- `1` → SECLO (conciliación prelegal)
- `2` → Demanda inicial (traslado, contestación)
- `3` → Prueba (apertura a prueba, testimonial, pericial)
- `4` → Sentencia (fallo, parte dispositiva)
- `5` → Desconocido

**Output:** `data/sentencias_etiquetadas.csv`

---

### **FASE 2: Preparación de Datos** (5-10 minutos)

```bash
python preparar_datos.py
```

**Qué hace:**
- Extrae texto completo de PDFs
- Limpia y normaliza texto
- Crea split train/test (80/20)
- Verifica balance de clases

**Output:**
- `data/processed/train.csv`
- `data/processed/test.csv`
- `data/processed/dataset_completo.csv`

---

### **FASE 3: Entrenamiento del Modelo** (2-5 minutos)

```bash
python entrenar_clasificador.py
```

**Qué hace:**
- Vectoriza texto con TF-IDF (1000 features, bi-gramas)
- Entrena Random Forest (100 árboles)
- Calcula métricas: Accuracy, F1-Score
- Genera matriz de confusión
- Identifica términos más importantes

**Output:**
- `models/vectorizer.pkl`
- `models/clasificador.pkl`
- `results/confusion_matrix.png`
- `results/metricas.csv`

**Métricas esperadas:**
- Accuracy: 70-85% (depende de calidad de datos)
- F1-Score: 0.65-0.80

---

### **FASE 4: Pruebas del Clasificador** (Opcional)

```bash
python probar_clasificador.py
```

**Opciones:**
1. Clasificar un PDF nuevo
2. Clasificar texto manual
3. Evaluar todos los PDFs de test

---

### **FASE 5: Sistema Integrado** (Prototipo Final)

```bash
python sistema_integrado.py
```

**Flujo completo:**
1. Usuario sube PDF
2. **Clasificador ML** identifica etapa procesal
3. **Generador** crea timeline de eventos pasados
4. **Generador** crea sugerencias de "cosas a tener en cuenta"
5. Guarda resultado en JSON

**Output:** `results/{nombre_pdf}_analisis.json`

---

## 📊 Componentes del Sistema

### 1. **Clasificador ML** (Componente Académico)
- **Algoritmo:** TF-IDF + Random Forest
- **Input:** Texto de documento procesal
- **Output:** Etapa + confianza
- **Métricas:** Accuracy, Precision, Recall, F1-Score

### 2. **Generador de Timeline** (Componente Funcional)
- **Input:** Etapa clasificada
- **Output:** Lista de eventos cronológicos
- **Tipos de eventos:**
  - Hitos cumplidos
  - Plazos críticos
  - Sugerencias y alertas

---

## 🎓 Para la Defensa de Tesis

### Capítulo de Metodología:

1. **Recolección de datos:** 50 sentencias laborales de CABA
2. **Etiquetado manual:** 5 categorías de etapas procesales
3. **Preprocesamiento:** Limpieza, normalización, train/test split
4. **Feature Engineering:** TF-IDF con bi-gramas, max 1000 features
5. **Modelo:** Random Forest (100 estimadores, depth=20)
6. **Evaluación:** Accuracy, F1-score, matriz de confusión

### Capítulo de Resultados:

- **Tabla de métricas:** Train vs Test accuracy
- **Gráfico:** Matriz de confusión (confusion_matrix.png)
- **Análisis:** Feature importance (top términos discriminantes)
- **Comparación:** Baseline vs modelo entrenado

### Limitaciones a mencionar:

- Dataset pequeño (50 documentos) - prototipo inicial
- Desbalance de clases posible
- Específico a CABA/Buenos Aires
- Requiere más datos para producción

---

## 🔧 Troubleshooting

### Error: "No se pudo extraer texto del PDF"
**Solución:** Verificar que el PDF tenga texto seleccionable (no sea imagen escaneada)

### Error: "Desbalance de clases severo"
**Solución:** Etiquetar más documentos de las clases minoritarias

### Warning: "Accuracy < 60%"
**Solución:** 
- Aumentar cantidad de datos
- Verificar calidad de etiquetas
- Ajustar hiperparámetros del modelo

---

## 📝 Notas para Desarrollo Futuro

### Mejoras posibles:
1. **Fine-tuning de LLM:** Usar Claude/GPT para generar texto más contextualizado
2. **Extracción de entidades:** NER para identificar actores, fechas, montos
3. **Predicción de plazos:** ML para calcular tiempos reales por juzgado
4. **Clasificación multi-label:** Identificar múltiples etapas en un documento
5. **Dataset público:** Crear corpus etiquetado para la comunidad

---

## 👥 Créditos

**Autora:** Mica  
**Universidad:** UADE  
**Proyecto:** LexGO - Sistema de Gestión Legal  
**Año:** 2024-2025

---

## 📄 Licencia

Este es un proyecto académico de tesis de grado.
