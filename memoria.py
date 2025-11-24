import os
import pandas as pd
import numpy as np
from oct2py import octave

# --- CONFIGURACIÓN ---
print("Iniciando motor de Octave...")
octave.addpath(os.getcwd()) # Para encontrar 'procesar.m'

def procesar_memoria_completa(ruta_dataset):
    datos_totales = []
    
    # Nombres de las carpetas padre (Singular, tal cual tu captura)
    categorias_principales = ['benigno', 'maligno']
    
    for categoria_padre in categorias_principales:
        ruta_padre = os.path.join(ruta_dataset, categoria_padre)
        
        if not os.path.exists(ruta_padre):
            print(f"[AVISO] No encuentro la carpeta: {ruta_padre}")
            continue

        # Detectar subcarpetas automáticamente (Angioma, Melanoma, etc.)
        subtipos = [d for d in os.listdir(ruta_padre) if os.path.isdir(os.path.join(ruta_padre, d))]
        
        for tipo_lunar in subtipos:
            ruta_tipo = os.path.join(ruta_padre, tipo_lunar)
            # Buscar imágenes jpg, png, jpeg (mayusculas o minusculas)
            archivos = [f for f in os.listdir(ruta_tipo) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            print(f"\n--- Procesando: {tipo_lunar} ({categoria_padre}) -> {len(archivos)} fotos ---")
            
            for archivo in archivos:
                ruta_img = os.path.join(ruta_tipo, archivo)
                try:
                    # 1. Llamada a Octave (Usando nout para evitar warnings)
                    area, perimetro, color, asimetria = octave.procesar(ruta_img, nout=4)
                    
                    # 2. Cálculo Circularidad
                    if perimetro > 0:
                        circularidad = (4 * np.pi * area) / (perimetro ** 2)
                    else:
                        circularidad = 0

                    # 3. Guardar datos
                    datos_totales.append({
                        'Area': area,
                        'Perimetro': perimetro,
                        'Circularidad': circularidad,
                        'Color_Std': color,
                        'Asimetria': asimetria,
                        # 0 = Benigno, 1 = Maligno
                        'Diagnostico_General': 0 if categoria_padre == 'benigno' else 1,
                        # Guardamos el nombre exacto de la carpeta (Ej: "Melanoma")
                        'Tipo_Especifico': tipo_lunar 
                    })
                    print(f"  [OK] {archivo}")
                    
                except Exception as e:
                    print(f"  [ERROR] {archivo}: {e}")

    return datos_totales

if __name__ == "__main__":
    print("--- INICIANDO ESCANEO COMPLETO ---")
    
    if os.path.exists('dataset'):
        data = procesar_memoria_completa('dataset')
        
        if len(data) > 0:
            df = pd.DataFrame(data)
            df.to_csv('memoria_entrenamiento.csv', index=False)
            print("\n" + "="*50)
            print("¡ÉXITO TOTAL!")
            print(f"Se generó 'memoria_entrenamiento.csv' con {len(df)} registros.")
            print("Distribución de datos:")
            print(df['Tipo_Especifico'].value_counts())
            print("="*50)
        else:
            print("\n[!] No se encontraron imágenes.")
    else:
        print("\n[!] Error: No encuentro la carpeta 'dataset'.")