import pandas as pd

print("--- LIMPIEZA AUTOMÁTICA DE DATOS ---")

try:
    df = pd.read_csv('memoria_entrenamiento.csv')
    total_inicial = len(df)
    print(f"Registros iniciales: {total_inicial}")
except:
    print("No encontré el archivo CSV.")
    exit()


df_limpio = df[df['Area'] > 200]

df_limpio = df_limpio[df_limpio['Circularidad'] > 0.05]

df_limpio = df_limpio[df_limpio['Asimetria'] > 0.01]

total_final = len(df_limpio)
borrados = total_inicial - total_final

print(f"\n🗑️  Se eliminaron {borrados} registros basura.")
print(f"✅ Registros útiles restantes: {total_final}")

df_limpio.to_csv('memoria_entrenamiento.csv', index=False)
print("Archivo sobrescrito y listo para re-entrenar.")