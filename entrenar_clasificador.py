"""
Entrenamiento del clasificador de etapas procesales
Tesis LexGO - Modelo ML con TF-IDF + Random Forest
"""

import pandas as pd
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    f1_score
)
import matplotlib.pyplot as plt
import seaborn as sns

def entrenar_modelo():
    """Entrena el clasificador ML"""
    
    print("🤖 ENTRENAMIENTO DEL CLASIFICADOR ML")
    print("=" * 60)
    
    # Cargar datos
    train_path = "data/processed/train.csv"
    test_path = "data/processed/test.csv"
    
    if not Path(train_path).exists():
        print("❌ No se encontró train.csv")
        print("   Primero ejecuta: python preparar_datos.py")
        return
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    print(f"\n✓ Train: {len(train_df)} documentos")
    print(f"✓ Test: {len(test_df)} documentos")
    
    X_train = train_df['texto']
    y_train = train_df['etapa']
    X_test = test_df['texto']
    y_test = test_df['etapa']
    
    # Vectorización con TF-IDF
    print("\n🔤 Vectorizando texto con TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=1000,      # Top 1000 palabras más importantes
        ngram_range=(1, 2),     # Unigramas y bigramas
        min_df=2,               # Palabra debe aparecer en al menos 2 docs
        max_df=0.8,             # Ignorar palabras muy frecuentes
        strip_accents='unicode',
        lowercase=True
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"   Vocabulario: {len(vectorizer.vocabulary_)} términos")
    print(f"   Matriz train: {X_train_tfidf.shape}")
    print(f"   Matriz test: {X_test_tfidf.shape}")
    
    # Ver términos más importantes
    feature_names = vectorizer.get_feature_names_out()
    print(f"\n🔝 Algunos términos del vocabulario:")
    print(f"   {list(feature_names[:10])}")
    
    # Entrenar Random Forest
    print("\n🌲 Entrenando Random Forest...")
    clf = RandomForestClassifier(
        n_estimators=100,       # 100 árboles
        max_depth=20,           # Profundidad máxima
        min_samples_split=5,    # Mínimo para split
        random_state=42,
        n_jobs=-1               # Usar todos los cores
    )
    
    clf.fit(X_train_tfidf, y_train)
    print("   ✓ Entrenamiento completado")
    
    # Predicciones
    print("\n🎯 Evaluando modelo...")
    y_train_pred = clf.predict(X_train_tfidf)
    y_test_pred = clf.predict(X_test_tfidf)
    
    # Métricas en train
    train_accuracy = accuracy_score(y_train, y_train_pred)
    print(f"\n📊 Accuracy Train: {train_accuracy:.3f}")
    
    # Métricas en test
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_f1 = f1_score(y_test, y_test_pred, average='weighted')
    
    print(f"📊 Accuracy Test: {test_accuracy:.3f}")
    print(f"📊 F1-Score Test: {test_f1:.3f}")
    
    # Classification Report
    print("\n📋 Reporte de Clasificación (Test):")
    print("-" * 60)
    report = classification_report(y_test, y_test_pred)
    print(report)
    
    # Matriz de confusión
    print("\n📊 Matriz de Confusión:")
    cm = confusion_matrix(y_test, y_test_pred)
    
    # Crear figura
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=clf.classes_,
        yticklabels=clf.classes_
    )
    plt.title('Matriz de Confusión - Clasificador de Etapas')
    plt.ylabel('Etapa Real')
    plt.xlabel('Etapa Predicha')
    plt.tight_layout()
    
    # Guardar figura
    Path("results").mkdir(exist_ok=True)
    plt.savefig('results/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("   ✓ Guardada en: results/confusion_matrix.png")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🎯 Top 20 términos más importantes:")
    print(feature_importance.head(20).to_string(index=False))
    
    # Guardar modelo
    print("\n💾 Guardando modelo...")
    Path("models").mkdir(exist_ok=True)
    
    with open('models/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    with open('models/clasificador.pkl', 'wb') as f:
        pickle.dump(clf, f)
    
    print("   ✓ models/vectorizer.pkl")
    print("   ✓ models/clasificador.pkl")
    
    # Guardar métricas
    metricas = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'test_f1_score': test_f1,
        'num_train': len(y_train),
        'num_test': len(y_test),
        'num_features': len(feature_names),
        'classes': list(clf.classes_)
    }
    
    metricas_df = pd.DataFrame([metricas])
    metricas_df.to_csv('results/metricas.csv', index=False)
    print("   ✓ results/metricas.csv")
    
    print("\n✅ ENTRENAMIENTO COMPLETADO")
    print("\n⏭️  Próximo paso: python probar_clasificador.py")
    
    return clf, vectorizer

def probar_ejemplo():
    """Prueba el modelo con un texto de ejemplo"""
    
    print("\n" + "=" * 60)
    print("🧪 PRUEBA CON TEXTO DE EJEMPLO")
    print("=" * 60)
    
    # Cargar modelo
    try:
        with open('models/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('models/clasificador.pkl', 'rb') as f:
            clf = pickle.load(f)
    except FileNotFoundError:
        print("❌ Modelo no encontrado. Primero entrena el modelo.")
        return
    
    # Textos de ejemplo
    ejemplos = [
        "se fija audiencia de conciliación en el marco del seclo para el día 15 de marzo",
        "córrese traslado de la demanda al demandado por el plazo de diez días",
        "se declara abierta a prueba la causa por el término de cuarenta días",
        "resuelvo hacer lugar a la demanda y condenar al demandado al pago de las sumas reclamadas"
    ]
    
    print("\nProbando ejemplos:")
    print("-" * 60)
    
    for i, texto in enumerate(ejemplos, 1):
        texto_vec = vectorizer.transform([texto])
        prediccion = clf.predict(texto_vec)[0]
        probabilidades = clf.predict_proba(texto_vec)[0]
        confianza = max(probabilidades)
        
        print(f"\n{i}. Texto: {texto[:60]}...")
        print(f"   → Predicción: {prediccion} (confianza: {confianza:.2%})")

if __name__ == "__main__":
    clf, vectorizer = entrenar_modelo()
    probar_ejemplo()
