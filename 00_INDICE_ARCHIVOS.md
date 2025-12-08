# 📦 ÍNDICE DE ARCHIVOS DEL PROYECTO
## LexGO ML Tesis - Sistema Clasificador de Etapas Procesales

**Fecha de generación:** 4 de Diciembre 2024  
**Total de archivos:** 10

---

## 📚 DOCUMENTACIÓN (4 archivos)

### 1. README.md (5.7 KB)
**Descripción:** Manual completo del proyecto  
**Contiene:**
- Estructura del proyecto
- Pipeline paso a paso
- Instrucciones de uso
- Troubleshooting
- Notas para desarrollo futuro

**Cuándo leer:** PRIMERO - antes de empezar

---

### 2. RESUMEN_EJECUTIVO.md (9.2 KB)
**Descripción:** Documento académico para tesis  
**Contiene:**
- Arquitectura del sistema
- Detalles técnicos del ML
- Métricas de evaluación
- Aporte académico
- Referencias bibliográficas

**Cuándo usar:** Para escribir capítulos de tesis

---

### 3. GUIA_RAPIDA.md (3.1 KB)
**Descripción:** Referencia rápida de una página  
**Contiene:**
- 5 pasos del proceso
- Categorías de etiquetado
- FAQ y troubleshooting
- Timeline de trabajo

**Cuándo usar:** Tenerlo a mano mientras trabajas

---

### 4. INSTALAR.bat (975 bytes)
**Descripción:** Script de instalación para Windows  
**Función:**
- Crea estructura de carpetas
- Verifica Python
- Instala dependencias

**Cómo usar:** Doble clic en Windows

---

## 🐍 SCRIPTS PYTHON (5 archivos)

### 5. etiquetar_sentencias.py (5.2 KB)
**Orden de ejecución:** #1  
**Función:** Etiquetado manual interactivo  
**Input:** PDFs en data/raw/  
**Output:** data/sentencias_etiquetadas.csv  
**Tiempo estimado:** 2-3 horas

**Características:**
- Preview automático de texto
- Sugerencias de categoría
- Auto-guardado cada 5 archivos
- Detección de keywords

---

### 6. preparar_datos.py (5.2 KB)
**Orden de ejecución:** #2  
**Función:** Procesamiento de datos  
**Input:** sentencias_etiquetadas.csv  
**Output:** train.csv, test.csv, dataset_completo.csv  
**Tiempo estimado:** 2-5 minutos

**Características:**
- Extracción de texto de PDFs
- Limpieza y normalización
- Train/test split (80/20)
- Verificación de balance de clases
- Estadísticas del dataset

---

### 7. entrenar_clasificador.py (6.6 KB)
**Orden de ejecución:** #3  
**Función:** Entrenamiento del modelo ML  
**Input:** train.csv, test.csv  
**Output:** vectorizer.pkl, clasificador.pkl, métricas  
**Tiempo estimado:** 2-5 minutos

**Características:**
- Vectorización TF-IDF
- Random Forest Classifier
- Métricas completas (Accuracy, F1, etc.)
- Matriz de confusión visual
- Feature importance
- Ejemplos de prueba

**⭐ COMPONENTE CLAVE PARA TESIS**

---

### 8. probar_clasificador.py (5.1 KB)
**Orden de ejecución:** #4 (opcional)  
**Función:** Testeo interactivo del modelo  
**Input:** PDF o texto manual  
**Output:** Predicción + probabilidades  
**Tiempo estimado:** Variable

**Características:**
- 3 modos de prueba
- Visualización de probabilidades
- Evaluación batch de test set

---

### 9. sistema_integrado.py (11 KB)
**Orden de ejecución:** #5 (prototipo final)  
**Función:** Sistema completo ML + Generador  
**Input:** PDF nuevo  
**Output:** JSON con timeline + sugerencias  
**Tiempo estimado:** <1 minuto por PDF

**Características:**
- Clasificación ML automática
- Generación de timeline de eventos
- Sugerencias contextualizadas
- Exportación a JSON
- Base de conocimiento procesal

**⭐ PROTOTIPO FINAL - DEMOSTRACIÓN**

---

### 10. setup_environment.py (1.2 KB)
**Orden de ejecución:** Auxiliar  
**Función:** Setup inicial de ambiente  
**Uso:** Opcional, alternativa a INSTALAR.bat

---

## 📊 FLUJO DE TRABAJO COMPLETO

```
1. INSTALAR.bat
   └─> Crea carpetas + instala librerías

2. Descargar 50 PDFs manualmente
   └─> Copiar a data/raw/

3. python etiquetar_sentencias.py
   └─> data/sentencias_etiquetadas.csv

4. python preparar_datos.py
   └─> data/processed/train.csv + test.csv

5. python entrenar_clasificador.py
   └─> models/ + results/

6. python probar_clasificador.py (opcional)
   └─> Verificar funcionamiento

7. python sistema_integrado.py
   └─> Prototipo final funcionando
```

---

## 🎯 ARCHIVOS CLAVE PARA DEFENSA DE TESIS

### Captura de pantalla:
1. ✅ Output de `entrenar_clasificador.py` (métricas)
2. ✅ Archivo `results/confusion_matrix.png`
3. ✅ Ejemplo de `sistema_integrado.py` (output completo)

### Documentos para escribir:
1. ✅ RESUMEN_EJECUTIVO.md → Metodología
2. ✅ README.md → Anexo técnico
3. ✅ Código fuente → Repositorio/Anexo

---

## ⚠️ IMPORTANTE

### Antes de empezar:
- [ ] Python 3.8+ instalado
- [ ] 50 PDFs de sentencias descargados
- [ ] 3-4 horas disponibles para etiquetar
- [ ] Leído el README.md completo

### Durante el proceso:
- [ ] Etiquetar cuidadosamente (calidad > velocidad)
- [ ] Revisar balance de clases después de etiquetar
- [ ] Verificar accuracy ≥ 60% en test
- [ ] Guardar screenshots de resultados

### Para la tesis:
- [ ] Documentar métricas obtenidas
- [ ] Mencionar limitaciones (dataset pequeño)
- [ ] Explicar decisiones técnicas (por qué Random Forest)
- [ ] Discutir trabajo futuro

---

## 📞 SOPORTE

**Para preguntas durante desarrollo:**
- Revisa GUIA_RAPIDA.md primero
- Consulta sección Troubleshooting en README.md
- Verifica que todos los archivos estén en sus carpetas

**Para defensa de tesis:**
- Usa RESUMEN_EJECUTIVO.md como base
- Prepara explicación de arquitectura híbrida
- Ten claras las métricas obtenidas

---

## ✅ CHECKLIST DE ENTREGA

### Código:
- [x] 10 archivos generados
- [x] Documentación completa
- [x] Instrucciones de instalación

### Funcionalidad:
- [ ] Sistema clasifica etapas correctamente
- [ ] Genera timeline por etapa
- [ ] Produce sugerencias contextuales
- [ ] Exporta resultados en JSON

### Evaluación:
- [ ] 50 PDFs etiquetados
- [ ] Train/test split documentado
- [ ] Métricas ≥ objetivos (70% accuracy)
- [ ] Resultados guardados en results/

---

**Estado del proyecto:** ✅ LISTO PARA USAR  
**Última actualización:** 4 de Diciembre 2024  
**Versión:** 1.0 - Prototipo Inicial

---

## 📥 PRÓXIMOS PASOS

1. **HOY:** 
   - Descargar estos 10 archivos
   - Ejecutar INSTALAR.bat
   - Descargar primeros 10 PDFs de prueba

2. **MAÑANA:**
   - Etiquetar los 50 PDFs completos
   - Ejecutar pipeline completo
   - Verificar métricas

3. **ESTA SEMANA:**
   - Documentar resultados para tesis
   - Preparar presentación
   - Probar sistema con casos reales

---

