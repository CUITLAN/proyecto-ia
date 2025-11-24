import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

def entrenar_sistema():
    print("Iniciando entrenamiento...")
    
    try:
        df = pd.read_csv('memoria_entrenamiento.csv')
        print(f"Registros cargados: {len(df)}")
    except FileNotFoundError:
        print("Error: Archivo 'memoria_entrenamiento.csv' no encontrado.")
        return

    X = df[['Area', 'Perimetro', 'Circularidad', 'Color_Std', 'Asimetria']]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("Entrenando modelo de Riesgo...")
    y_riesgo = df['Diagnostico_General'] # 0: Benigno, 1: Maligno
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_scaled, y_riesgo, test_size=0.2, random_state=42, stratify=y_riesgo
    )
    
    modelo_riesgo = RandomForestClassifier(n_estimators=300, max_depth=20, random_state=42, class_weight='balanced')
    modelo_riesgo.fit(X_train_r, y_train_r)
    
    acc_riesgo = accuracy_score(y_test_r, modelo_riesgo.predict(X_test_r))
    print(f"Precisión Modelo Riesgo: {acc_riesgo*100:.2f}%")

    print("Entrenando modelo de Tipos Específicos...")
    y_texto = df['Tipo_Especifico']
    
    encoder = LabelEncoder()
    y_especifico = encoder.fit_transform(y_texto)
    
    X_train_e, X_test_e, y_train_e, y_test_e = train_test_split(
        X_scaled, y_especifico, test_size=0.2, random_state=42, stratify=y_especifico
    )
    
    modelo_especifico = RandomForestClassifier(n_estimators=300, class_weight='balanced', random_state=42)
    modelo_especifico.fit(X_train_e, y_train_e)
    
    acc_especifico = accuracy_score(y_test_e, modelo_especifico.predict(X_test_e))
    print(f"Precisión Modelo Específico: {acc_especifico*100:.2f}%")

    print("Guardando archivos .pkl...")
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(modelo_riesgo, 'cerebro_riesgo.pkl')
    joblib.dump(modelo_especifico, 'cerebro_nombres.pkl')
    joblib.dump(encoder, 'traductor.pkl')
    
    print("Proceso finalizado correctamente.")

if __name__ == "__main__":
    entrenar_sistema()