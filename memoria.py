import os
import pandas as pd
import numpy as np
from oct2py import octave

# --- CONFIGURACIÓN INICIAL ---
print("Iniciando motor de Octave...")
# Añadimos la ruta actual. IMPORTANTE: octave.procesar debe existir en esta carpeta.
octave.addpath(os.getcwd()) 

def procesar_memoria_completa(ruta_dataset):
    datos_totales = []
    
    # Nombres de carpetas tal cual salen en tu captura (Singular)
    categorias_principales = ['benigno', 'maligno']
    
    for categoria_padre in categorias_principales:
        ruta_padre = os.path.join(ruta_dataset, categoria_padre)
        
        if not os.path.exists(ruta_padre):
            print(f"[AVISO] No encuentro la carpeta: {ruta_padre}")
            continue

        # Busamos subcarpetas (Angioma, Nevus, etc.)
        subtipos = [d for d in os.listdir(ruta_padre) if os.path.isdir(os.path.join(ruta_padre, d))]
        
        for tipo_lunar in subtipos:
            ruta_tipo = os.path.join(ruta_padre, tipo_lunar)
            archivos = [f for f in os.listdir(ruta_tipo) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            print(f"\n--- Procesando: {tipo_lunar} ({categoria_padre}) -> {len(archivos)} fotos ---")
            
            for archivo in archivos:
                ruta_img = os.path.join(ruta_tipo, archivo)
                try:
                    # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
                    # 1. Llamamos a 'procesar' (el archivo nuevo procesar.m)
                    # 2. Usamos 'nout=4' para evitar el warning de Python
                    area, perimetro, color, asimetria = octave.procesar(ruta_img, nout=4)
                    
                    # Calculo Python (Circularidad)
                    if perimetro > 0:
                        circularidad = (4 * np.pi * area) / (perimetro ** 2)
                    else:
                        circularidad = 0

                    datos_totales.append({
                        'Area': area,
                        'Perimetro': perimetro,
                        'Circularidad': circularidad,
                        'Color_Std': color,
                        'Asimetria': asimetria,
                        'Diagnostico_General': 0 if categoria_padre == 'benigno' else 1,
                        'Tipo_Especifico': tipo_lunar
                    })
                    print(f"  [OK] {archivo}")
                    
                except Exception as e:
                    print(f"  [ERROR] {archivo}: {e}")

    return datos_totales

# --- EJECUCIÓN ---
if __name__ == "__main__":
    print("--- INICIANDO ESCANEO DE MEMORIA ---")
    
    # Verifica que tengas la carpeta 'dataset' al lado de este archivo
    if os.path.exists('dataset'):
        data = procesar_memoria_completa('dataset')
        
        if len(data) > 0:
            df = pd.DataFrame(data)
            df.to_csv('memoria_entrenamiento.csv', index=False)
            print("\n" + "="*50)
            print("¡MEMORIA GENERADA CON ÉXITO!")
            print(f"Se guardaron {len(df)} registros.")
            print(df.head())
            print("="*50)
        else:
            print("\n[!] No se encontraron imágenes válidas.")
    else:
        print("\n[!] Error: No encuentro la carpeta 'dataset'.")