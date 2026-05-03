# Possum Regression Predictor - Development Guide 
https://pt2-1-ihus.onrender.com/
## Project Structure

```
PT2/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── static/
│   └── style.css         # CSS styling
├── templates/
│   └── index.html        # Frontend UI
└── data/
    ├── possum.csv        # Training data
    └── prediction_output.csv  # Prediction storage (auto-generated)
```

## Setup & Running

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

## Development Notes

### Backend (Flask)

- **app.py**: Main Flask application with prediction logic
- Uses pre-trained linear regression model coefficients
- CSV-based persistence in `data/prediction_output.csv`
- CORS enabled for development

### Frontend (HTML/CSS/JS)

- **static/style.css**: Responsive glassmorphism design
- **templates/index.html**: Single-page application
- Vanilla JavaScript with Chart.js for visualizations
- Real-time API calls to backend

### API Endpoints

#### GET /api/predictions

Returns all stored predictions

```json
{
  "success": true,
  "data": [...],
  "count": 5
}
```

#### POST /api/predict

Submit new measurement and get prediction

```json
{
  "total": 87,
  "tail": 36,
  "skull": 56,
  "chest": 28,
  "belly": 35,
  "sex": "male"
}
```

Response:

```json
{
  "success": true,
  "predicted": 93.36,
  "message": "Prediction saved to CSV"
}
```

#### POST /api/clear

Clear all predictions (development only)

## CSV Format

Data saved in `data/prediction_output.csv`:

```
Total Length,Tail Length,Skull Width,Chest Girth,Belly Girth,Sex,Predicted Head Length
87,36,56,28,35,Male,93.36
```

## Features

✅ Real-time prediction model
✅ Automatic CSV persistence
✅ Interactive data visualization (Chart.js)
✅ Responsive design
✅ REST API backend
✅ Form validation
✅ Error handling

## Troubleshooting

### Port Already in Use

If port 5000 is busy:

```bash
# Change port in app.py: app.run(port=8000)
```

### CSV File Errors

- Auto-created in `data/` folder on first run
- Delete `data/prediction_output.csv` to reset

### CORS Errors

- Already handled via Flask-CORS
- Works cross-origin in development

## Next Steps for Production

1. Use Gunicorn or uWSGI instead of Flask dev server
2. Add database (SQLite/PostgreSQL) instead of CSV
3. Implement user authentication
4. Add input validation on frontend
5. Set up proper logging
6. Add unit tests

## Development Commands

```bash
# Run with debug logging
python app.py

# Test API endpoint
curl http://localhost:5000/api/predictions
```

---

**Status**: Development-Ready ✅
├── possum.csv # Original training data
├── prediction_output.csv # CSV file where predictions are saved
├── requirements.txt # Python dependencies
├── OpenIntro_Possum_Regression_Birju.ipynb # Jupyter notebook with model training
└── README.md # This file

````

## Features

✅ **Multivariate Linear Regression** - Predicts possum head length from 6 features
✅ **Real-time CSV Persistence** - New predictions automatically saved to `prediction_output.csv`
✅ **Interactive Dashboard** - Charts, statistics, and data table
✅ **Model Coefficients Matched** - Uses the exact coefficients from the trained notebook model
✅ **Full-Stack Architecture** - Python Flask backend + HTML5/JavaScript frontend

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
````

This installs:

- Flask (web server)
- Flask-CORS (cross-origin requests)
- scikit-learn (machine learning)
- numpy (numerical computing)

### 2. Start the Backend Server

```bash
python app.py
```

You should see:

```
Starting Possum Regression Predictor...
Serving on http://localhost:5000
CSV file: C:\Users\birju\OneDrive\Desktop\PT2\prediction_output.csv
```

The server runs on **http://localhost:5000**

### 3. Open the Frontend

Once the server is running, open your browser and navigate to:

```
http://localhost:5000
```

## How It Works

### Frontend (Index.html)

- Displays form to enter possum measurements
- Shows interactive charts (Actual vs Predicted, Residuals)
- Displays table of all saved predictions
- Sends prediction requests to the backend API

### Backend (app.py)

- **GET `/api/predictions`** - Loads all predictions from `prediction_output.csv`
- **POST `/api/predict`** - Receives new measurement data, makes prediction, saves to CSV
- **POST `/api/clear`** - Clears all predictions (for testing)

### Model Details

The linear regression model uses:

- **6 Input Features**: Total Length, Tail Length, Skull Width, Chest Girth, Belly Girth, Sex
- **Target Variable**: Head Length (mm)
- **Model Type**: LinearRegression with StandardScaler normalization
- **R² Score**: 0.597 (moderate fit)
- **RMSE**: 1.752 mm

**Feature Scaling Parameters** (from training data):

```
Means:  total=86.95, tail=36.85, skull=56.24, chest=26.98, belly=32.45
StdDev: total=4.98,  tail=2.15,  skull=3.45,  chest=2.41,  belly=3.27
```

**Model Coefficients** (standardized features):

```
coef = [0.524, 0.187, 0.891, 0.312, 0.228, 0.764]
intercept = 92.58
```

## Testing the Application

### Manual Testing

1. Enter sample values in the form
2. Click "Predict & Save to CSV" button
3. New row appears in the table
4. Prediction is automatically saved to `prediction_output.csv`

### Test Data

The app comes with sample predictions already in `prediction_output.csv`:

```
Total Length, Tail Length, Skull Width, Chest Girth, Belly Girth, Sex, Predicted Head Length
87, 36, 56, 28, 35, male, 93.36
92.0, 36.0, 58.0, 30.0, 37.0, male, 96.8
...
```

### Example Prediction

**Input:**

- Total Length: 87 cm
- Tail Length: 36 cm
- Skull Width: 56 mm
- Chest Girth: 28 cm
- Belly Girth: 35 cm
- Sex: male

**Output:** ~93.36 mm predicted head length ✓

## API Endpoints

### GET /api/predictions

Returns all saved predictions

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "total": 87,
      "tail": 36,
      "skull": 56,
      "chest": 28,
      "belly": 35,
      "sex": "male",
      "predictedHead": 93.36
    }
  ],
  "count": 1
}
```

### POST /api/predict

Save a new prediction

**Request:**

```json
{
  "total": 87,
  "tail": 36,
  "skull": 56,
  "chest": 28,
  "belly": 35,
  "sex": "male"
}
```

**Response:**

```json
{
  "success": true,
  "predicted": 93.36,
  "message": "Prediction saved to prediction_output.csv"
}
```

### POST /api/clear

Clear all predictions (for testing only)

**Response:**

```json
{
  "success": true,
  "message": "All predictions cleared"
}
```

## CSV File Format

The `prediction_output.csv` file has the following columns:

```
Total Length,Tail Length,Skull Width,Chest Girth,Belly Girth,Sex,Predicted Head Length
```

Each new prediction is automatically appended to this file by the backend server.

## Troubleshooting

### "Could not load from API" error

- Ensure the Flask server is running on port 5000
- Check that `http://localhost:5000` is accessible in your browser
- Look for error messages in the terminal where you ran `python app.py`

### Predictions not saving to CSV

- Check the file path in `app.py` - it should match your project location
- Ensure the CSV file is not locked by another application
- Check file permissions - the directory should be writable

### Port 5000 already in use

- Close other applications using port 5000
- Or modify the port in `app.py`: `app.run(debug=True, host='localhost', port=5001)`

## Technologies Used

- **Backend**: Python 3, Flask, scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript (vanilla), Chart.js
- **Data Format**: CSV
- **ML Model**: LinearRegression with StandardScaler

## Project Files Description

| File                                      | Purpose                                        |
| ----------------------------------------- | ---------------------------------------------- |
| `app.py`                                  | Flask backend server with API endpoints        |
| `Index.html`                              | Interactive web frontend with forms and charts |
| `possum.csv`                              | Original training dataset (104 observations)   |
| `prediction_output.csv`                   | Output file storing all predictions            |
| `requirements.txt`                        | Python package dependencies                    |
| `OpenIntro_Possum_Regression_Birju.ipynb` | Jupyter notebook with model training details   |

## Notes

- The application runs entirely on your local machine (localhost)
- All predictions are permanently saved to `prediction_output.csv`
- The frontend automatically refreshes data from the backend when you make a prediction
- Charts and statistics update in real-time as you add new predictions

## Future Enhancements

- Export predictions to Excel/PDF
- Advanced filtering and sorting options
- Model retraining with new data
- Prediction confidence intervals
- Historical trend analysis

---

**Author:** Birju  
**Created:** May 2, 2026  
**Dataset:** OpenIntro Possum Dataset
