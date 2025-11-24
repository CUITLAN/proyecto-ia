import os
from oct2py import octave

print("Iniciando auditoría visual...")
octave.addpath(os.getcwd())

# CAMBIA ESTO POR LA RUTA DE UNA FOTO QUE TÚ TENGAS
ruta_prueba = "dataset/maligno/Melanoma/Melanoma1.png"

if os.path.exists(ruta_prueba):
    print(f"Procesando: {ruta_prueba}")
    # El '1' al final activa el modo debug en Octave
    octave.procesar(ruta_prueba, 1, nout=4)
    print("✅ ¡Listo! Revisa el archivo 'octave_debug_view.jpg' que apareció en tu carpeta.")
else:
    print("La imagen no existe.")