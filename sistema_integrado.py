"""
Sistema Integrado: Clasificador ML + LLM
Genera timeline de eventos y sugerencias basadas en etapa procesal
Tesis LexGO - Prototipo final
"""

import pickle
import PyPDF2
import json
from pathlib import Path
from datetime import datetime, timedelta

# Para usar la API de Claude (deberás instalar: pip install anthropic)
# import anthropic

def cargar_modelo():
    """Carga el clasificador ML entrenado"""
    try:
        with open('models/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        with open('models/clasificador.pkl', 'rb') as f:
            clf = pickle.load(f)
        return vectorizer, clf
    except FileNotFoundError:
        print("❌ Modelo no encontrado")
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
        return None

def clasificar_etapa(texto, vectorizer, clf):
    """Clasifica la etapa procesal usando ML"""
    texto_vec = vectorizer.transform([texto.lower()])
    prediccion = clf.predict(texto_vec)[0]
    probabilidades = clf.predict_proba(texto_vec)[0]
    confianza = max(probabilidades)
    
    return prediccion, confianza

# Eventos predefinidos según etapa (sin usar LLM, solo lógica)
EVENTOS_POR_ETAPA = {
    'seclo': [
        {
            'titulo': 'Presentación en SECLO',
            'descripcion': 'Reclamo presentado ante el Servicio de Conciliación Laboral Obligatoria',
            'dias_desde_inicio': 0,
            'tipo': 'hito'
        },
        {
            'titulo': 'Notificación al empleador',
            'descripcion': 'El SECLO notifica al empleador mediante cédula',
            'dias_desde_inicio': 7,
            'tipo': 'hito'
        },
        {
            'titulo': 'Audiencia de conciliación SECLO',
            'descripcion': 'Audiencia obligatoria de conciliación prelegal',
            'dias_desde_inicio': 20,
            'tipo': 'audiencia'
        },
        {
            'titulo': 'Cosas a tener en cuenta',
            'descripcion': 'Sugerencias: Preparar toda la documentación laboral (recibos, telegrama). Si hay acuerdo, puede homologarse ante Ministerio. Si fracasa, tendrá 90 días para demandar judicialmente.',
            'tipo': 'sugerencia'
        }
    ],
    'demanda_inicial': [
        {
            'titulo': 'Certificado habilitante SECLO',
            'descripcion': 'Se obtuvo certificado de fracaso de conciliación',
            'dias_desde_inicio': 0,
            'tipo': 'hito'
        },
        {
            'titulo': 'Presentación de demanda judicial',
            'descripcion': 'Demanda presentada ante Juzgado Laboral',
            'dias_desde_inicio': 30,
            'tipo': 'hito'
        },
        {
            'titulo': 'Sorteo y traslado',
            'descripcion': 'Juzgado asignado y traslado notificado al demandado (10 días para contestar)',
            'dias_desde_inicio': 35,
            'tipo': 'hito'
        },
        {
            'titulo': 'Vencimiento contestación',
            'descripcion': 'Plazo para que el demandado conteste la demanda',
            'dias_desde_inicio': 50,
            'tipo': 'plazo_critico'
        },
        {
            'titulo': 'Cosas a tener en cuenta',
            'descripcion': 'Sugerencias: Verificar que la demanda incluya certificado SECLO. El traslado es un plazo perentorio de 10 días hábiles. La incomparecencia del demandado puede generar confesión ficta. Preparar para audiencia Art. 58.',
            'tipo': 'sugerencia'
        }
    ],
    'prueba': [
        {
            'titulo': 'Eventos previos',
            'descripcion': 'Ya se realizó SECLO, demanda, contestación y audiencia Art. 58',
            'dias_desde_inicio': 0,
            'tipo': 'resumen'
        },
        {
            'titulo': 'Apertura a prueba',
            'descripcion': 'Causa abierta a prueba por 40 días hábiles',
            'dias_desde_inicio': 60,
            'tipo': 'hito'
        },
        {
            'titulo': 'Producción de prueba',
            'descripcion': 'Período para producir prueba documental, pericial, testimonial',
            'dias_desde_inicio': 65,
            'tipo': 'hito'
        },
        {
            'titulo': 'Clausura de prueba',
            'descripcion': 'Vencimiento del plazo de 40 días hábiles',
            'dias_desde_inicio': 120,
            'tipo': 'plazo_critico'
        },
        {
            'titulo': 'Cosas a tener en cuenta',
            'descripcion': 'Sugerencias: Gestionar oficios a AFIP, ANSES, ART si corresponde. Coordinar peritos contadores. Citar testigos con anticipación. Monitorear reiteraciones de oficios. El plazo de 40 días es perentorio.',
            'tipo': 'sugerencia'
        }
    ],
    'sentencia': [
        {
            'titulo': 'Proceso completo realizado',
            'descripcion': 'Se completaron todas las etapas: SECLO, demanda, prueba, alegatos',
            'dias_desde_inicio': 0,
            'tipo': 'resumen'
        },
        {
            'titulo': 'Alegatos presentados',
            'descripcion': 'Las partes presentaron sus alegatos sobre el mérito de la prueba',
            'dias_desde_inicio': 150,
            'tipo': 'hito'
        },
        {
            'titulo': 'Llamamiento de autos',
            'descripcion': 'Expediente a despacho del juez para dictar sentencia',
            'dias_desde_inicio': 160,
            'tipo': 'hito'
        },
        {
            'titulo': 'Sentencia de primera instancia',
            'descripcion': 'El juez dicta sentencia resolviendo la causa',
            'dias_desde_inicio': 250,
            'tipo': 'hito'
        },
        {
            'titulo': 'Cosas a tener en cuenta',
            'descripcion': 'Sugerencias: Analizar si la sentencia es favorable, parcial o desfavorable. Evaluar viabilidad de recurso de apelación (5 días hábiles). Si es favorable, preparar liquidación de condena. Si es desfavorable, preparar expresión de agravios. Considerar costas del proceso.',
            'tipo': 'sugerencia'
        }
    ],
    'desconocido': [
        {
            'titulo': 'Etapa no identificada',
            'descripcion': 'No se pudo determinar la etapa procesal con certeza',
            'tipo': 'advertencia'
        },
        {
            'titulo': 'Cosas a tener en cuenta',
            'descripcion': 'Sugerencias: Revisar manualmente el documento. Verificar que sea un documento procesal laboral de CABA/Buenos Aires. Consultar con un abogado laboralista para identificar correctamente la etapa.',
            'tipo': 'sugerencia'
        }
    ]
}

def generar_timeline_eventos(etapa_predicha):
    """Genera timeline de eventos según la etapa (sin LLM, lógica pura)"""
    eventos = EVENTOS_POR_ETAPA.get(etapa_predicha, EVENTOS_POR_ETAPA['desconocido'])
    return eventos

def generar_timeline_con_fechas(eventos, fecha_inicio=None):
    """Agrega fechas estimadas a los eventos"""
    if fecha_inicio is None:
        fecha_inicio = datetime.now()
    
    timeline = []
    for evento in eventos:
        evento_copia = evento.copy()
        
        if 'dias_desde_inicio' in evento:
            fecha_estimada = fecha_inicio + timedelta(days=evento['dias_desde_inicio'])
            evento_copia['fecha_estimada'] = fecha_estimada.strftime('%d/%m/%Y')
        
        timeline.append(evento_copia)
    
    return timeline

def guardar_resultado(pdf_filename, etapa_predicha, confianza, timeline):
    """Guarda el resultado en JSON"""
    resultado = {
        'archivo': pdf_filename,
        'timestamp': datetime.now().isoformat(),
        'clasificacion': {
            'etapa': etapa_predicha,
            'confianza': float(confianza)
        },
        'timeline': timeline
    }
    
    # Guardar en results
    output_path = Path('results') / f'{Path(pdf_filename).stem}_analisis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    return output_path

def main():
    """Sistema integrado completo"""
    
    print("🚀 SISTEMA INTEGRADO: CLASIFICADOR ML + GENERADOR DE TIMELINE")
    print("=" * 70)
    
    # Cargar modelo ML
    vectorizer, clf = cargar_modelo()
    if vectorizer is None:
        return
    
    print("✓ Modelo ML cargado")
    
    # Solicitar PDF
    pdf_path = input("\n📄 Ruta del PDF a analizar: ").strip()
    
    if not Path(pdf_path).exists():
        print(f"❌ No se encontró: {pdf_path}")
        return
    
    # Paso 1: Extraer texto
    print("\n🔄 Paso 1/3: Extrayendo texto del PDF...")
    texto = extract_text_from_pdf(pdf_path)
    
    if not texto:
        print("❌ No se pudo extraer texto")
        return
    
    print(f"✓ Extraídos {len(texto)} caracteres")
    
    # Paso 2: Clasificar con ML
    print("\n🤖 Paso 2/3: Clasificando etapa procesal (Modelo ML)...")
    etapa_predicha, confianza = clasificar_etapa(texto, vectorizer, clf)
    
    print(f"✓ Etapa identificada: {etapa_predicha}")
    print(f"✓ Confianza: {confianza:.1%}")
    
    # Paso 3: Generar timeline
    print("\n📅 Paso 3/3: Generando timeline de eventos...")
    eventos = generar_timeline_eventos(etapa_predicha)
    timeline = generar_timeline_con_fechas(eventos)
    
    print(f"✓ {len(timeline)} eventos generados")
    
    # Mostrar resultado
    print("\n" + "=" * 70)
    print("📊 RESULTADO DEL ANÁLISIS")
    print("=" * 70)
    print(f"\n📄 Archivo: {Path(pdf_path).name}")
    print(f"🎯 Etapa procesal: {etapa_predicha.upper()}")
    print(f"📈 Confianza: {confianza:.1%}")
    
    print(f"\n📅 TIMELINE DE EVENTOS:")
    print("-" * 70)
    
    for i, evento in enumerate(timeline, 1):
        if evento['tipo'] == 'sugerencia':
            print(f"\n💡 {evento['titulo']}:")
            print(f"   {evento['descripcion']}")
        elif evento['tipo'] == 'plazo_critico':
            fecha = evento.get('fecha_estimada', 'N/A')
            print(f"\n⚠️  {i}. {evento['titulo']} ({fecha})")
            print(f"   {evento['descripcion']}")
        else:
            fecha = evento.get('fecha_estimada', 'N/A')
            print(f"\n{i}. {evento['titulo']} ({fecha})")
            print(f"   {evento['descripcion']}")
    
    # Guardar resultado
    output_path = guardar_resultado(pdf_path, etapa_predicha, confianza, timeline)
    
    print("\n" + "=" * 70)
    print(f"💾 Resultado guardado en: {output_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
