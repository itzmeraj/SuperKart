import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the serialized model pipeline on startup
model_path = 'superkart_sales_prediction_model.pkl'
try:
    model_pipeline = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model_pipeline = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model_pipeline:
        return jsonify({'error': 'Model pipeline is not loaded on the backend'}), 500

    try:
        # Get JSON payload
        data = request.get_json(force=True)

        # Convert inputs into a pandas DataFrame
        # Expecting dict of features, e.g. {'Product_Weight': [12.5], ...}
        input_df = pd.DataFrame(data)

        # Run prediction
        prediction = model_pipeline.predict(input_df)

        # Return predictions as list
        return jsonify({
            'predictions': prediction.tolist(),
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model_pipeline is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)