import os
import joblib
import numpy as np
from oct2py import octave
import warnings
import json

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Cargando. . . ")

SISTEMA_OK = False

try:
    octave.addpath(BASE_DIR)
    
    scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
    ia_riesgo = joblib.load(os.path.join(BASE_DIR, 'cerebro_riesgo.pkl'))
    ia_nombres = joblib.load(os.path.join(BASE_DIR, 'cerebro_nombres.pkl'))
    traductor = joblib.load(os.path.join(BASE_DIR, 'traductor.pkl'))
    
    SISTEMA_OK = True
    print("Sistema cargado ")

except Exception as e:
    print(f"Error cargando modelos: {e}")

def analizar_imagen(ruta_imagen):
    if not os.path.exists(ruta_imagen):
        return {"error": "El archivo de imagen no existe."}
    
    if not SISTEMA_OK:
        return {"error": "El sistema de IA no se pudo cargar correctamente."}

    try:
        try:
            area, perimetro, color, asimetria = octave.procesar(ruta_imagen, 0, nout=4)
        except Exception as oct_err:
            return {"error": f"Error procesando imagen en Octave: {oct_err}"}
        
        if perimetro > 0:
            circularidad = (4 * np.pi * area) / (perimetro ** 2)
        else:
            circularidad = 0

        raw_features = np.array([[area, perimetro, circularidad, color, asimetria]])
        
        features_scaled = scaler.transform(raw_features)

        pred_riesgo = ia_riesgo.predict(features_scaled)[0] 
        prob_riesgo = ia_riesgo.predict_proba(features_scaled)[0]
        confianza_riesgo = prob_riesgo[pred_riesgo] * 100
        
        es_maligno = (pred_riesgo == 1)
        
        pred_nombre_idx = ia_nombres.predict(features_scaled)[0]
        nombre_lunar = traductor.inverse_transform([pred_nombre_idx])[0]
        
        resultado = {
            "status": "success",
            "diagnostico_riesgo": "MALIGNO" if es_maligno else "BENIGNO",
            "confianza": f"{confianza_riesgo:.1f}%",
            "tipo_detectado": nombre_lunar,
            "color_ui": "red" if es_maligno else "green",
            "mensaje": " Luce algo riesgoso" if es_maligno else "Todo bien todo correcto",
            "datos_tecnicos": {
                "Area": int(area),
                "Perimetro": int(perimetro),
                "Asimetria": round(asimetria, 3),
                "Color_Std": round(color, 2)
            }
        }

        return resultado

    except Exception as e:
        return {"error": f"Error internio {str(e)}"}

if __name__ == "__main__":
    print("Ando esperando el input")
    
    ruta_prueba = "prueba.png"
    
    if os.path.exists(ruta_prueba):
        print(f"\nProcesando: {ruta_prueba}")
        respuesta = analizar_imagen(ruta_prueba)
        print(json.dumps(respuesta, indent=4))
    else:
        print(f"\nNo encontré la imagen de prueba: {ruta_prueba}")