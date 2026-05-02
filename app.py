#!/usr/bin/env python3
"""
Flask backend for Possum Regression Predictor
Serves the frontend and handles CSV data persistence
Development-ready with proper project structure
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
CORS(app)

# Configuration
CSV_FILE = 'data/prediction_output.csv'
CSV_HEADERS = ["Total Length", "Tail Length", "Skull Width", "Chest Girth", "Belly Girth", "Sex", "Predicted Head Length"]

# Pre-trained model coefficients (from notebook training)
MODEL_MEANS = {'totlngth': 86.95, 'taill': 36.85, 'skullw': 56.24, 'chest': 26.98, 'belly': 32.45}
MODEL_STDS = {'totlngth': 4.98, 'taill': 2.15, 'skullw': 3.45, 'chest': 2.41, 'belly': 3.27}
MODEL_COEF = [0.524, 0.187, 0.891, 0.312, 0.228, 0.764]
MODEL_INTERCEPT = 92.58


def predict_head_length(total, tail, skull, chest, belly, sex):
    """Predict head length using pre-trained linear regression model"""
    z_tot = (total - MODEL_MEANS['totlngth']) / MODEL_STDS['totlngth']
    z_tail = (tail - MODEL_MEANS['taill']) / MODEL_STDS['taill']
    z_skull = (skull - MODEL_MEANS['skullw']) / MODEL_STDS['skullw']
    z_chest = (chest - MODEL_MEANS['chest']) / MODEL_STDS['chest']
    z_belly = (belly - MODEL_MEANS['belly']) / MODEL_STDS['belly']
    sex_enc = 1 if sex.lower() == 'male' else 0
    
    prediction = (MODEL_INTERCEPT + 
                 MODEL_COEF[0] * z_tot + 
                 MODEL_COEF[1] * z_tail + 
                 MODEL_COEF[2] * z_skull + 
                 MODEL_COEF[3] * z_chest + 
                 MODEL_COEF[4] * z_belly + 
                 MODEL_COEF[5] * sex_enc)
    
    return max(80, min(105, prediction))


def ensure_csv_exists():
    """Ensure data folder and CSV file exist with headers"""
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def read_all_predictions():
    """Read all predictions from CSV"""
    ensure_csv_exists()
    predictions = []
    try:
        with open(CSV_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    try:
                        predictions.append({
                            'total': float(row['Total Length']),
                            'tail': float(row['Tail Length']),
                            'skull': float(row['Skull Width']),
                            'chest': float(row['Chest Girth']),
                            'belly': float(row['Belly Girth']),
                            'sex': row['Sex'],
                            'predictedHead': float(row['Predicted Head Length'])
                        })
                    except (ValueError, KeyError):
                        continue
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return list(reversed(predictions))


def save_prediction(total, tail, skull, chest, belly, sex, predicted):
    """Append new prediction to CSV"""
    ensure_csv_exists()
    try:
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([total, tail, skull, chest, belly, sex, round(predicted, 2)])
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False


# Routes
@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return render_template('index.html')


@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """API endpoint to get all predictions"""
    try:
        predictions = read_all_predictions()
        return jsonify({
            'success': True,
            'data': predictions,
            'count': len(predictions)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def make_prediction():
    """API endpoint to make prediction and save to CSV"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['total', 'tail', 'skull', 'chest', 'belly', 'sex']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Parse inputs
        total = float(data['total'])
        tail = float(data['tail'])
        skull = float(data['skull'])
        chest = float(data['chest'])
        belly = float(data['belly'])
        sex = data['sex'].strip().lower()
        
        # Validate sex
        if sex not in ['male', 'female']:
            return jsonify({'success': False, 'error': 'Sex must be male or female'}), 400
        
        # Make prediction
        predicted = predict_head_length(total, tail, skull, chest, belly, sex)
        
        # Save to CSV
        success = save_prediction(total, tail, skull, chest, belly, sex.title(), predicted)
        
        if success:
            return jsonify({
                'success': True,
                'predicted': round(predicted, 2),
                'message': 'Prediction saved to CSV'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save prediction'}), 500
    
    except ValueError as e:
        return jsonify({'success': False, 'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_predictions():
    """Clear all predictions (testing only)"""
    try:
        ensure_csv_exists()
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        return jsonify({'success': True, 'message': 'All predictions cleared'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Possum Regression Predictor - Development Server")
    print("=" * 60)
    print(f"CSV storage: {os.path.abspath(CSV_FILE)}")
    print(f"API URL: http://localhost:5000")
    print(f"Press CTRL+C to stop")
    print("=" * 60)
    app.run(debug=True, host='localhost', port=5000)
