import os
import joblib
import json
import numpy as np
from oct2py import octave
import warnings

# Limpiar consola
warnings.filterwarnings("ignore")

print("--- INICIANDO PRUEBA DE DIAGNÓSTICO ---")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    octave.addpath(BASE_DIR)
    
    scaler = joblib.load('scaler.pkl')
    ia_riesgo = joblib.load('cerebro_riesgo.pkl')
    ia_nombres = joblib.load('cerebro_nombres.pkl')
    traductor = joblib.load('traductor.pkl')
    
    print("sistema de Doble Capa cargado")
except Exception as e:
    print(f"Error cargando arcivos: {e}")
    exit()

def probar_foto(ruta_imagen):
   
    
    try:
        
        area, perimetro, color, asimetria = octave.procesar(ruta_imagen, 0, nout=4)
        
        if perimetro > 0:
            circularidad = (4 * np.pi * area) / (perimetro ** 2)
        else:
            circularidad = 0
            
        raw_features = np.array([[area, perimetro, circularidad, color, asimetria]])
        
        features_scaled = scaler.transform(raw_features)
        
        
        pred_riesgo = ia_riesgo.predict(features_scaled)[0] # 0 o 1
        prob_riesgo = ia_riesgo.predict_proba(features_scaled)[0]
        confianza = max(prob_riesgo) * 100
        
        es_maligno = (pred_riesgo == 1)
        
        pred_nombre_idx = ia_nombres.predict(features_scaled)[0]
        nombre_lunar = traductor.inverse_transform([pred_nombre_idx])[0]

        resultado = {
            "archivo": os.path.basename(ruta_imagen),
            "diagnostico": "MALIGNO" if es_maligno else "BENIGNO",
            "tipo_detectado": nombre_lunar,
            "confianza_riesgo": f"{confianza:.2f}%",
            "datos_tecnicos": {
                "Area": int(area),
                "Asimetria": round(asimetria, 4),
                "Color": round(color, 2)
            }
        }
        return json.dumps(resultado, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    
    ruta_fija = "prueba.png"
    
    if os.path.exists(ruta_fija):
        print(probar_foto(ruta_fija))
    else:
        print(f"❌ No encuentro la imagen: {ruta_fija}")