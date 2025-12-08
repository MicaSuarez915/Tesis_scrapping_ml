"""
Herramienta de etiquetado manual rápido para sentencias laborales
Tesis LexGO - Clasificador de Etapas Procesales
"""

import pandas as pd
from pathlib import Path
import PyPDF2
import csv

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
        print(f"❌ Error en {pdf_path}: {e}")
        return None

def main():
    """Proceso de etiquetado interactivo"""
    
    # Carpeta con PDFs descargados
    pdf_folder = Path("data/raw")
    output_file = "data/sentencias_etiquetadas.csv"
    
    # Categorías de etapa
    categorias = {
        '1': 'seclo',
        '2': 'demanda_inicial', 
        '3': 'prueba',
        '4': 'sentencia',
        '5': 'desconocido'
    }
    
    print("🏷️  ETIQUETADOR DE SENTENCIAS LABORALES")
    print("=" * 60)
    print("\nCategorías disponibles:")
    for key, value in categorias.items():
        print(f"  {key} → {value}")
    print("\n  's' → Saltar archivo")
    print("  'q' → Guardar y salir")
    print("=" * 60)
    
    # Cargar etiquetas existentes si hay
    labeled_data = []
    if Path(output_file).exists():
        df_existing = pd.read_csv(output_file)
        labeled_data = df_existing.to_dict('records')
        print(f"\n✓ Cargadas {len(labeled_data)} etiquetas previas")
    
    # Obtener archivos ya etiquetados
    labeled_files = {item['filename'] for item in labeled_data}
    
    # Procesar PDFs
    pdf_files = list(pdf_folder.glob("*.pdf"))
    pending_files = [f for f in pdf_files if f.name not in labeled_files]
    
    print(f"\n📊 Total PDFs: {len(pdf_files)}")
    print(f"✅ Ya etiquetados: {len(labeled_files)}")
    print(f"⏳ Pendientes: {len(pending_files)}")
    print("\n" + "=" * 60 + "\n")
    
    for i, pdf_path in enumerate(pending_files, 1):
        print(f"\n📄 Archivo {i}/{len(pending_files)}: {pdf_path.name}")
        print("-" * 60)
        
        # Extraer y mostrar preview del texto
        text = extract_text_from_pdf(pdf_path)
        
        if text is None:
            print("⚠️  No se pudo extraer texto, saltando...")
            continue
        
        # Mostrar preview (primeros 500 caracteres)
        preview = text[:500].replace('\n', ' ')
        print(f"\n📝 Preview:\n{preview}...\n")
        
        # Buscar keywords automáticamente
        keywords = {
            'seclo': ['seclo', 'conciliación previa', 'certificado habilitante', 'audiencia conciliatoria'],
            'demanda_inicial': ['traslado de la demanda', 'córrese traslado', 'contestación de demanda'],
            'prueba': ['apertura a prueba', 'testimonial', 'pericial', 'producción de prueba'],
            'sentencia': ['resuelvo', 'se hace lugar', 'se rechaza', 'parte dispositiva']
        }
        
        text_lower = text.lower()
        suggestions = []
        for etapa, words in keywords.items():
            if any(word in text_lower for word in words):
                suggestions.append(etapa)
        
        if suggestions:
            print(f"💡 Sugerencias automáticas: {', '.join(suggestions)}")
        
        # Solicitar etiqueta
        while True:
            etiqueta = input("\n🏷️  Categoría (1-5, s=saltar, q=salir): ").strip().lower()
            
            if etiqueta == 'q':
                print("\n💾 Guardando y saliendo...")
                # Guardar antes de salir
                df = pd.DataFrame(labeled_data)
                df.to_csv(output_file, index=False)
                print(f"✅ {len(labeled_data)} etiquetas guardadas en {output_file}")
                return
            
            if etiqueta == 's':
                print("⏭️  Saltando archivo...")
                break
            
            if etiqueta in categorias:
                # Agregar etiqueta
                labeled_data.append({
                    'filename': pdf_path.name,
                    'etapa': categorias[etiqueta],
                    'texto': text[:1000]  # Guardar solo preview del texto
                })
                print(f"✅ Etiquetado como: {categorias[etiqueta]}")
                
                # Guardar incrementalmente cada 5 archivos
                if len(labeled_data) % 5 == 0:
                    df = pd.DataFrame(labeled_data)
                    df.to_csv(output_file, index=False)
                    print(f"💾 Auto-guardado: {len(labeled_data)} etiquetas")
                break
            else:
                print("❌ Opción inválida, intenta de nuevo")
    
    # Guardar al final
    if labeled_data:
        df = pd.DataFrame(labeled_data)
        df.to_csv(output_file, index=False)
        print(f"\n✅ COMPLETADO: {len(labeled_data)} sentencias etiquetadas")
        print(f"📊 Archivo guardado: {output_file}")
        
        # Mostrar distribución
        print("\n📈 Distribución de etiquetas:")
        print(df['etapa'].value_counts())
    else:
        print("\n⚠️  No se etiquetaron archivos")

if __name__ == "__main__":
    main()