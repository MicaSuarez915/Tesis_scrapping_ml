# 🚀 GUÍA RÁPIDA - USO DEL SISTEMA

## ⚡ Inicio Rápido (5 pasos)

### 1️⃣ INSTALAR (Una sola vez)
```bash
# Windows: doble clic en INSTALAR.bat
# O manualmente:
pip install pypdf2 pandas scikit-learn matplotlib seaborn
```

### 2️⃣ ETIQUETAR (2-3 horas)
```bash
python etiquetar_sentencias.py
```
- Coloca 50 PDFs en `data/raw/`
- Presiona 1-5 para clasificar cada uno
- Guarda cada 5 archivos automáticamente

### 3️⃣ PREPARAR DATOS (2 minutos)
```bash
python preparar_datos.py
```
- Procesa PDFs etiquetados
- Crea train.csv y test.csv

### 4️⃣ ENTRENAR MODELO (2 minutos)
```bash
python entrenar_clasificador.py
```
- Entrena Random Forest
- Genera métricas y gráficos
- Guarda modelo en `models/`

### 5️⃣ USAR SISTEMA COMPLETO
```bash
python sistema_integrado.py
```
- Ingresa ruta de PDF
- Recibe: etapa + timeline + sugerencias

---

## 📁 Estructura de Archivos

```
lexgo-ml-tesis/
├── data/
│   ├── raw/              ← Coloca aquí tus PDFs
│   └── processed/        ← Se genera automáticamente
├── models/               ← Modelo entrenado
├── results/              ← Gráficos y métricas
└── [scripts .py]         ← 5 scripts principales
```

---

## 🎯 Categorías de Etiquetado

| # | Etapa | Palabras Clave |
|---|-------|----------------|
| 1 | SECLO | "seclo", "conciliación previa" |
| 2 | Demanda Inicial | "traslado", "córrese traslado" |
| 3 | Prueba | "apertura a prueba", "testimonial" |
| 4 | Sentencia | "resuelvo", "se hace lugar" |
| 5 | Desconocido | No estás seguro |

---

## 📊 Métricas que Verás

- **Accuracy:** % de predicciones correctas
- **F1-Score:** Balance entre precisión y cobertura
- **Matriz de confusión:** Errores por categoría

**Objetivo:** Accuracy ≥ 70%, F1 ≥ 0.65

---

## ❓ Preguntas Frecuentes

**Q: ¿Cuántos PDFs necesito mínimo?**  
A: 40-50 para prototipo inicial

**Q: ¿Qué hago si mi accuracy es < 60%?**  
A: Revisa etiquetas, agrega más datos, ajusta parámetros

**Q: ¿Puedo cambiar el modelo?**  
A: Sí, en `entrenar_clasificador.py` línea 47

**Q: ¿Cómo interpreto la matriz de confusión?**  
A: Diagonal = aciertos, fuera = errores

---

## 🆘 Troubleshooting

| Error | Solución |
|-------|----------|
| "No such file" | Verifica ruta del PDF |
| "No se pudo extraer texto" | PDF es imagen, usa OCR |
| Import error | Reinstala: `pip install [librería]` |
| Accuracy muy bajo | Necesitas más datos |

---

## 📝 Para Tu Tesis

### Captura de pantalla importante:
1. Output de `entrenar_clasificador.py` (métricas)
2. Gráfico `confusion_matrix.png`
3. Output de `sistema_integrado.py` (ejemplo)

### Menciona en defensa:
- Dataset: 50 docs, train/test 80/20
- Modelo: TF-IDF + Random Forest
- Resultados: Accuracy X%, F1 Y%
- Limitaciones: Dataset pequeño, solo CABA

---

## ⏱️ Timeline Total

- Etiquetado: 2-3 horas
- Procesamiento: 5 min
- Entrenamiento: 5 min
- Pruebas: 30 min
- Documentación: 1 hora

**TOTAL: ~4 horas de trabajo efectivo**

---

**Versión 1.0** | Micaela Suárez | UADE 2025
