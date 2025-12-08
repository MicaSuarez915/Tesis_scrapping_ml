# RESUMEN EJECUTIVO - PROYECTO ML
## Clasificador de Etapas Procesales Laborales

**Proyecto:** LexGO - Sistema de Gestión Legal  
**Objetivo:** Objetivo 4 de Tesis  
**Autor:** Mica | UADE 2024-2025

---

## 🎯 OBJETIVO DEL PROTOTIPO

Desarrollar un prototipo inicial de modelo predictivo basado en técnicas de machine learning que:
- Sugiera estructuras básicas de causas legales
- Alerte sobre posibles errores u omisiones
- Sea evaluado en un entorno de prueba controlado

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Enfoque: Híbrido ML Tradicional + Generación Inteligente

```
┌─────────────────────────────────────────────────────────────┐
│                   INPUT: PDF Legal                          │
│              (Sentencia, Demanda, Acta)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         PASO 1: Extracción de Texto (PyPDF2)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│    PASO 2: CLASIFICADOR ML (Componente Académico)          │
│                                                             │
│    • Vectorización: TF-IDF (1000 features, bi-gramas)      │
│    • Modelo: Random Forest (100 árboles, depth=20)         │
│    • Clases: seclo, demanda_inicial, prueba, sentencia     │
│    • Output: Etapa + Confianza                             │
│                                                             │
│    🎓 Métricas de evaluación:                               │
│       - Train/Test split (80/20)                            │
│       - Accuracy, Precision, Recall, F1-Score               │
│       - Matriz de confusión                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│   PASO 3: GENERADOR DE TIMELINE (Componente Funcional)     │
│                                                             │
│    • Input: Etapa clasificada por ML                        │
│    • Lógica: Base de conocimiento de proceso laboral       │
│    • Output: Timeline de eventos + sugerencias             │
│                                                             │
│    📅 Genera:                                               │
│       - Eventos históricos (lo que ya pasó)                 │
│       - Plazos críticos (lo que viene)                      │
│       - Sugerencias y alertas (errores u omisiones)         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              OUTPUT: Análisis Completo                      │
│         (JSON con timeline + sugerencias)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 COMPONENTE ML - DETALLES TÉCNICOS

### Dataset
- **Tamaño:** 50 sentencias laborales (CABA/Buenos Aires)
- **Fuente:** CIJ, bases públicas de jurisprudencia
- **Etiquetado:** Manual, 5 categorías
- **Split:** 80% train (40 docs), 20% test (10 docs)

### Preprocesamiento
1. Extracción de texto de PDFs
2. Limpieza: minúsculas, normalización de espacios
3. Tokenización automática

### Feature Engineering
- **Técnica:** TF-IDF (Term Frequency - Inverse Document Frequency)
- **Parámetros:**
  - max_features: 1000 (vocabulario)
  - ngram_range: (1, 2) → unigramas y bigramas
  - min_df: 2 → palabra debe aparecer en ≥2 documentos
  - max_df: 0.8 → ignorar palabras muy frecuentes

### Modelo de Clasificación
- **Algoritmo:** Random Forest Classifier
- **Justificación:** 
  - Robusto ante overfitting
  - Maneja datos desbalanceados
  - Interpretable (feature importance)
- **Hiperparámetros:**
  - n_estimators: 100 árboles
  - max_depth: 20
  - min_samples_split: 5

### Métricas de Evaluación
- **Accuracy:** Porcentaje de predicciones correctas
- **Precision:** De los predichos como X, cuántos son realmente X
- **Recall:** De los que son X, cuántos fueron detectados
- **F1-Score:** Media armónica de precision y recall
- **Matriz de Confusión:** Visualización de errores por clase

**Objetivo:** Accuracy ≥ 70%, F1-Score ≥ 0.65

---

## ⚙️ COMPONENTE GENERADOR - TIMELINE

### Entrada
Etapa procesal clasificada por ML + nivel de confianza

### Base de Conocimiento
Diccionario estructurado con eventos por etapa basado en:
- Ley 24.635 (SECLO)
- Ley 18.345 (Procedimiento Laboral)
- Prácticas procesales CABA

### Salida
JSON estructurado con:
```json
{
  "clasificacion": {
    "etapa": "prueba",
    "confianza": 0.87
  },
  "timeline": [
    {
      "titulo": "Apertura a prueba",
      "descripcion": "Causa abierta a prueba por 40 días hábiles",
      "fecha_estimada": "15/03/2025",
      "tipo": "hito"
    },
    {
      "titulo": "Cosas a tener en cuenta",
      "descripcion": "Sugerencias: Gestionar oficios a AFIP...",
      "tipo": "sugerencia"
    }
  ]
}
```

### Tipos de Eventos
- **Hitos:** Eventos ya ocurridos
- **Plazos críticos:** Fechas límite importantes
- **Sugerencias:** Errores u omisiones a considerar
- **Advertencias:** Alertas de riesgo procesal

---

## 🧪 EVALUACIÓN DEL PROTOTIPO

### Criterios de Éxito
1. **Funcionalidad:** Sistema procesa PDF → identifica etapa → genera timeline
2. **Precisión ML:** Accuracy ≥ 70% en test set
3. **Utilidad práctica:** Timeline contiene eventos relevantes
4. **Robustez:** Maneja documentos de diferentes formatos

### Casos de Prueba
- **20 documentos de test** controlados
- **Métricas cuantitativas:** Accuracy, F1-Score
- **Evaluación cualitativa:** Relevancia de sugerencias

### Ambiente de Prueba
- Python 3.8+
- Scikit-learn 1.0+
- Dataset etiquetado manualmente
- Validación cruzada

---

## 📈 RESULTADOS ESPERADOS

### Componente ML
- **Accuracy Train:** 85-95% (puede haber overfitting leve)
- **Accuracy Test:** 70-85% (métrica clave)
- **F1-Score:** 0.65-0.80

### Componente Generador
- **Completitud:** 100% de timelines tienen sugerencias
- **Relevancia:** Eventos corresponden a la etapa identificada
- **Precisión:** Fechas estimadas basadas en plazos legales reales

---

## 🎓 APORTE ACADÉMICO

### Cumplimiento del Objetivo 4
✅ Desarrollar prototipo inicial  
✅ Basado en técnicas de machine learning  
✅ Sugiere estructuras de causas (timeline de eventos)  
✅ Alerta sobre errores (sugerencias contextualizadas)  
✅ Evaluado en entorno de prueba controlado

### Innovación
- **Híbrido:** Combina ML supervisado + generación basada en conocimiento
- **Práctico:** Resuelve problema real de abogados juniors
- **Escalable:** Arquitectura permite agregar más etapas/tipos de casos
- **Reproducible:** Dataset y código documentados

### Limitaciones (a mencionar en tesis)
- Dataset pequeño (50 docs) - suficiente para prototipo
- Alcance limitado a derecho laboral CABA/Buenos Aires
- Clasificación de una sola etapa (no multietapa)
- Sugerencias basadas en reglas (no generadas por LLM)

---

## 🔮 TRABAJO FUTURO

1. **Expandir dataset:** 200-500 documentos
2. **Fine-tuning LLM:** Usar Claude/GPT para sugerencias personalizadas
3. **Multi-clasificación:** Identificar múltiples etapas en un documento
4. **Extracción de entidades:** NER para actores, fechas, montos
5. **Predicción de plazos:** ML para estimar tiempos reales por juzgado

---

## 📚 REFERENCIAS

- Ley 24.635: SECLO - Etapa prelegal obligatoria
- Ley 18.345: Procedimiento Laboral
- Scikit-learn: Machine Learning in Python (Pedregosa et al., 2011)
- Bases públicas: CIJ, SAIJ

---

**Documento preparado para:** Defensa de Tesis  
**Fecha:** Diciembre 2024  
**Versión:** 1.0 - Prototipo Inicial
