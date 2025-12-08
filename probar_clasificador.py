"""
Probador interactivo del clasificador de etapas procesales
Tesis LexGO - Testing del modelo ML
"""

import pickle
import PyPDF2
from pathlib import Path

def cargar_modelo():
    """Carga el modelo entrenado"""
    try:
        with open('models/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('models/clasificador.pkl', 'rb') as f:
            clf = pickle.load(f)
        return vectorizer, clf
    except FileNotFoundError:
        print("❌ Modelo no encontrado")
        print("   Primero ejecuta: python entrenar_clasificador.py")
        return None, None

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def clasificar_texto(texto, vectorizer, clf):
    """Clasifica un texto y retorna predicción con probabilidades"""
    texto_vec = vectorizer.transform([texto.lower()])
    prediccion = clf.predict(texto_vec)[0]
    probabilidades = clf.predict_proba(texto_vec)[0]
    
    # Obtener todas las clases con sus probabilidades
    clases_probs = list(zip(clf.classes_, probabilidades))
    clases_probs_sorted = sorted(clases_probs, key=lambda x: x[1], reverse=True)
    
    return prediccion, clases_probs_sorted

def main():
    """Probador interactivo"""
    
    print("🧪 PROBADOR DEL CLASIFICADOR DE ETAPAS")
    print("=" * 60)
    
    # Cargar modelo
    vectorizer, clf = cargar_modelo()
    if vectorizer is None:
        return
    
    print("✓ Modelo cargado correctamente")
    print(f"✓ Clases disponibles: {clf.classes_}")
    
    print("\n📋 Opciones:")
    print("  1. Clasificar un PDF")
    print("  2. Clasificar texto manual")
    print("  3. Evaluar todos los PDFs de test")
    print("  q. Salir")
    print("=" * 60)
    
    while True:
        opcion = input("\n➤ Selecciona opción: ").strip().lower()
        
        if opcion == 'q':
            print("👋 ¡Hasta luego!")
            break
        
        elif opcion == '1':
            # Clasificar PDF
            pdf_path = input("\n📄 Ruta del PDF (ej: data/raw/sentencia_001.pdf): ").strip()
            
            if not Path(pdf_path).exists():
                print(f"❌ No se encontró: {pdf_path}")
                continue
            
            print("\n🔄 Extrayendo texto...")
            texto = extract_text_from_pdf(pdf_path)
            
            if texto:
                print(f"✓ Texto extraído: {len(texto)} caracteres")
                print("\n📝 Preview:")
                print(texto[:300] + "...\n")
                
                prediccion, clases_probs = clasificar_texto(texto, vectorizer, clf)
                
                print("🎯 RESULTADO:")
                print(f"   Etapa predicha: {prediccion}")
                print(f"\n📊 Probabilidades:")
                for clase, prob in clases_probs:
                    barra = "█" * int(prob * 30)
                    print(f"   {clase:20s}: {prob:.2%} {barra}")
        
        elif opcion == '2':
            # Clasificar texto manual
            print("\n✏️  Escribe o pega el texto (Enter dos veces para terminar):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            
            texto = " ".join(lines)
            
            if texto:
                prediccion, clases_probs = clasificar_texto(texto, vectorizer, clf)
                
                print("\n🎯 RESULTADO:")
                print(f"   Etapa predicha: {prediccion}")
                print(f"\n📊 Probabilidades:")
                for clase, prob in clases_probs:
                    barra = "█" * int(prob * 30)
                    print(f"   {clase:20s}: {prob:.2%} {barra}")
        
        elif opcion == '3':
            # Evaluar todos los test
            import pandas as pd
            
            test_path = "data/processed/test.csv"
            if not Path(test_path).exists():
                print("❌ No se encontró test.csv")
                continue
            
            test_df = pd.read_csv(test_path)
            
            print(f"\n🔄 Evaluando {len(test_df)} documentos de test...\n")
            
            correctos = 0
            for idx, row in test_df.iterrows():
                prediccion, _ = clasificar_texto(row['texto'], vectorizer, clf)
                correcto = prediccion == row['etapa']
                correctos += correcto
                
                simbolo = "✓" if correcto else "✗"
                print(f"{simbolo} {idx+1}/{len(test_df)}: Real={row['etapa']}, Predicho={prediccion}")
            
            accuracy = correctos / len(test_df)
            print(f"\n📊 Accuracy en test: {accuracy:.2%} ({correctos}/{len(test_df)})")
        
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
