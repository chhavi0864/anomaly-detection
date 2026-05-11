from flask import Flask, request, jsonify
import joblib
import os
import pandas as pd
import io

# Initialize Flask app
app = Flask(__name__)

# Load Machine Learning artifacts
MODEL_PATH = 'models/model.joblib'
SCALER_PATH = 'models/scaler.joblib'
FEATURES_PATH = 'models/features.joblib'

# Explicitly define the 78 features expected by the model
EXPECTED_FEATURES = [
    'Destination Port', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max', 
    'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 
    'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 
    'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 
    'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 
    'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 
    'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 
    'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length', 
    'Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length', 
    'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 
    'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 
    'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 
    'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 
    'Fwd Header Length.1', 'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 
    'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 
    'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 
    'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'Init_Win_bytes_forward', 
    'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward', 
    'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 
    'Idle Std', 'Idle Max', 'Idle Min'
]

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    try:
        feature_columns = joblib.load(FEATURES_PATH)
    except FileNotFoundError:
        print("Warning: features.joblib not found, falling back to hardcoded list.")
        feature_columns = EXPECTED_FEATURES
    print("Successfully loaded ML models and scaler!")
except FileNotFoundError:
    print("Warning: Model files not found. Please ensure they exist in the models/ directory.")
    model = None
    scaler = None
    feature_columns = None

from flask import render_template

# Add a home route that serves the frontend
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
        
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400
        
    try:
        # Read the uploaded CSV
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        df = pd.read_csv(stream)
        
        # Strip column names
        df.columns = df.columns.str.strip()
        
        # Check if model artifacts are loaded
        if not feature_columns:
            return jsonify({'error': 'Model artifacts not loaded on the server'}), 500
            
        # 1. Check for missing columns
        missing_cols = [col for col in feature_columns if col not in df.columns]
        if missing_cols:
            return jsonify({'error': f'Missing required columns: {missing_cols}'}), 400
            
        # 2. Reorder columns to match training features (this also automatically drops extra columns)
        df = df[feature_columns]
        
        # 3. Convert data to numeric and drop NaN rows
        import numpy as np
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except (ValueError, TypeError):
                pass
        df.dropna(inplace=True)
        
        if df.empty:
            return jsonify({'error': 'Uploaded CSV contains no valid data after cleaning'}), 400
            
        # 4. Scale the data using the loaded scaler
        X_scaled = scaler.transform(df)
        
        # 5. Predict using the trained model
        predictions = model.predict(X_scaled)
        
        # 6. Convert -1 to 'Anomaly' and 1 to 'Normal'
        pred_labels = ['Anomaly' if p == -1 else 'Normal' for p in predictions]
        
        # 7. Calculate summary counts
        counts = pd.Series(pred_labels).value_counts().to_dict()
        
        # 8. Return results as JSON
        return jsonify({
            'total_processed': len(pred_labels),
            'counts': counts,
            'predictions': pred_labels
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
