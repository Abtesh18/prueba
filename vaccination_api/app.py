from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Ruta del archivo CSV
CSV_FILE_PATH = 'C:/Users/btesh/OneDrive/Escritorio/project/vaccination_api/data/vaccination_data.csv'

# Cargar el archivo CSV y limpiar los datos
def load_data():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        df.dropna(how='all', inplace=True)  # Elimina filas completamente vacías
        return df
    except FileNotFoundError:
        return None

# Ruta base
@app.route('/')
def home():
    return render_template('index.html')

# Obtener todos los datos de vacunación
@app.route('/api/v1/vaccination', methods=['GET'])
def get_vaccination_data():
    df = load_data()
    if df is None:
        return jsonify({"error": "Archivo de datos no encontrado"}), 500
    data = df.to_dict(orient='records')
    return jsonify(data)

# Obtener datos de vacunación por año específico
@app.route('/api/v1/vaccination/<int:year>', methods=['GET'])
def get_vaccination_by_year(year):
    df = load_data()
    if df is None:
        return jsonify({"error": "Archivo de datos no encontrado"}), 500

    year_column = f'{year} [YR{year}]'
    if year_column not in df.columns:
        return jsonify({"error": "Año no encontrado"}), 404

    data = []
    for _, row in df.iterrows():
        data.append({
            "pais": row['Country Name'],
            "año": year,
            "cobertura": row[year_column]
        })
    
    return jsonify(data)

# Obtener estadísticas generales de vacunación
@app.route('/api/v1/vaccination/stats', methods=['GET'])
def get_vaccination_stats():
    df = load_data()
    if df is None:
        return jsonify({"error": "Archivo de datos no encontrado"}), 500

    # Filtrar las columnas que contienen datos de cobertura por año
    coverage_columns = [col for col in df.columns if col.endswith('[YR1990]') or col.endswith('[YR2000]') or col.endswith('[YR2023]')]

    # Convertir los datos a tipo numérico, forzando errores a NaN
    coverage_data = pd.to_numeric(df[coverage_columns].values.flatten(), errors='coerce')
    
    # Eliminar valores nulos
    coverage_data = coverage_data[~pd.isnull(coverage_data)]
    
    # Calcular estadísticas
    stats = {
        "cobertura_media": coverage_data.mean(),
        "cobertura_minima": coverage_data.min(),
        "cobertura_maxima": coverage_data.max()
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)

