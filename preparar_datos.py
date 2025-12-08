"""
Preparación de datos para entrenamiento del clasificador
Tesis LexGO - Procesamiento de sentencias etiquetadas
"""

import pandas as pd
import PyPDF2
from pathlib import Path
import re
from sklearn.model_selection import train_test_split

def extract_full_text(pdf_path):
    """Extrae texto completo de un PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"❌ Error extrayendo {pdf_path}: {e}")
        return None

def clean_text(text):
    """Limpia y normaliza el texto"""
    if not text:
        return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Remover saltos de línea múltiples
    text = re.sub(r'\n+', ' ', text)
    
    # Remover espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    # Remover caracteres especiales pero mantener puntuación importante
    text = re.sub(r'[^\w\s\.,;:()\-]', '', text)
    
    return text.strip()

def main():
    """Procesa sentencias etiquetadas y crea dataset de entrenamiento"""
    
    print("📊 PREPARACIÓN DE DATOS PARA ENTRENAMIENTO")
    print("=" * 60)
    
    # Cargar etiquetas
    etiquetas_file = "data/sentencias_etiquetadas.csv"
    
    if not Path(etiquetas_file).exists():
        print(f"❌ No se encontró {etiquetas_file}")
        print("   Primero ejecuta etiquetar_sentencias.py")
        return
    
    df_etiquetas = pd.read_csv(etiquetas_file)
    print(f"\n✓ Cargadas {len(df_etiquetas)} etiquetas")
    
    # Mostrar distribución
    print("\n📈 Distribución de etiquetas:")
    print(df_etiquetas['etapa'].value_counts())
    
    # Extraer texto completo de cada PDF
    print("\n🔄 Extrayendo texto completo de PDFs...")
    textos_completos = []
    etapas = []
    archivos_procesados = []
    
    for idx, row in df_etiquetas.iterrows():
        pdf_path = Path("data/raw") / row['filename']
        
        if not pdf_path.exists():
            print(f"⚠️  No encontrado: {row['filename']}")
            continue
        
        texto = extract_full_text(pdf_path)
        
        if texto:
            texto_limpio = clean_text(texto)
            textos_completos.append(texto_limpio)
            etapas.append(row['etapa'])
            archivos_procesados.append(row['filename'])
            
            if (idx + 1) % 10 == 0:
                print(f"   Procesados: {idx + 1}/{len(df_etiquetas)}")
    
    print(f"\n✅ Textos extraídos: {len(textos_completos)}")
    
    # Crear DataFrame procesado
    df_procesado = pd.DataFrame({
        'filename': archivos_procesados,
        'texto': textos_completos,
        'etapa': etapas
    })
    
    # Estadísticas del texto
    df_procesado['longitud_texto'] = df_procesado['texto'].str.len()
    df_procesado['num_palabras'] = df_procesado['texto'].str.split().str.len()
    
    print("\n📊 Estadísticas del texto:")
    print(f"   Longitud promedio: {df_procesado['longitud_texto'].mean():.0f} caracteres")
    print(f"   Palabras promedio: {df_procesado['num_palabras'].mean():.0f} palabras")
    print(f"   Texto más corto: {df_procesado['longitud_texto'].min()} caracteres")
    print(f"   Texto más largo: {df_procesado['longitud_texto'].max()} caracteres")
    
    # Verificar balance de clases
    print("\n⚖️  Balance de clases:")
    conteo_etapas = df_procesado['etapa'].value_counts()
    for etapa, count in conteo_etapas.items():
        porcentaje = (count / len(df_procesado)) * 100
        print(f"   {etapa}: {count} ({porcentaje:.1f}%)")
    
    # Advertencia si hay desbalance severo
    min_clase = conteo_etapas.min()
    max_clase = conteo_etapas.max()
    ratio = max_clase / min_clase if min_clase > 0 else float('inf')
    
    if ratio > 3:
        print(f"\n⚠️  ADVERTENCIA: Desbalance de clases detectado (ratio {ratio:.1f}:1)")
        print("   Considera recolectar más datos de las clases minoritarias")
    
    # Train/Test Split
    print("\n🔀 Creando split train/test (80/20)...")
    X = df_procesado['texto']
    y = df_procesado['etapa']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # Mantiene proporción de clases
    )
    
    print(f"   Train: {len(X_train)} documentos")
    print(f"   Test: {len(X_test)} documentos")
    
    # Guardar datasets procesados
    train_df = pd.DataFrame({'texto': X_train, 'etapa': y_train})
    test_df = pd.DataFrame({'texto': X_test, 'etapa': y_test})
    
    train_df.to_csv('data/processed/train.csv', index=False)
    test_df.to_csv('data/processed/test.csv', index=False)
    
    # Guardar dataset completo también
    df_procesado.to_csv('data/processed/dataset_completo.csv', index=False)
    
    print("\n💾 Archivos guardados:")
    print("   ✓ data/processed/train.csv")
    print("   ✓ data/processed/test.csv")
    print("   ✓ data/processed/dataset_completo.csv")
    
    print("\n✅ PREPARACIÓN COMPLETADA")
    print("\n⏭️  Próximo paso: python entrenar_clasificador.py")

if __name__ == "__main__":
    main()
