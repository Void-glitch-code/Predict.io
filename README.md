# California Housing Price Predictor

A full-stack machine learning web application that predicts California housing prices using demographic and geographic features.



Built with:
* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Machine Learning:** Scikit-learn Random Forest Regressor
* **Data Processing:** Pandas, NumPy
* **Visualization:** Interactive prediction insights

---

## Features

### Real-time House Price Prediction
Predict median housing prices based on user inputs such as:
* Longitude & Latitude
* Median income
* Housing median age
* Total rooms & bedrooms
* Population & households
* Ocean proximity

---

### Interactive Dashboard
Modern UI with:
* Prediction metrics
* Price per room analysis
* Price-to-income ratio
* Population density insights
* Historical prediction tracking

---

### Backend API Integration
FastAPI-powered REST endpoints for:
* Prediction requests
* Data validation
* Model inference
* Error handling

---

## Tech Stack

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | Streamlit             |
| Backend         | FastAPI               |
| ML Model        | RandomForestRegressor |
| Data Processing | Pandas, NumPy         |
| Serialization   | Joblib                |
| Cloud Hosting   | Render + Streamlit Cloud |

---

## Project Structure

```bash
california-housing-predictor/
│
├── app.py                          # Streamlit frontend
├── api.py                          # FastAPI backend
├── model_loader.py                 # Custom transformer definitions + model loader
├── my_california_housing_model.pkl # Trained sklearn pipeline
├── train_model.ipynb               # Model training notebook
├── requirements.txt
├── .env                            # Local environment variables (not committed)
├── .gitignore
└── README.md
```

---

## Installation

### Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/california-housing-predictor.git
cd california-housing-predictor
```

---

### Create Virtual Environment
```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Configure Environment

Create a `.env` file in the project root:

```
API_URL=http://127.0.0.1:8000
```

> For cloud deployment, this is set via Streamlit Cloud secrets — see the [Deployment](#deployment) section.

---

## Run Backend
```bash
uvicorn api:app --reload
```

Backend runs on: `http://127.0.0.1:8000`

API docs available at: `http://127.0.0.1:8000/docs`

---

## Run Frontend
```bash
streamlit run app.py
```

Frontend runs on: `http://localhost:8501`

---

## Model Training

Train or retrain using:
```bash
train_model.ipynb
```

The notebook handles:
* Data preprocessing
* Feature engineering
* Model training
* Evaluation
* Exporting trained artifacts

---

## Example Prediction Inputs

| Feature            | Example   |
| ------------------ | --------- |
| Longitude          | -122.23   |
| Latitude           | 37.88     |
| Median Income      | 8.32      |
| Housing Median Age | 41        |
| Total Rooms        | 880       |
| Total Bedrooms     | 129       |
| Population         | 322       |
| Households         | 126       |
| Ocean Proximity    | NEAR BAY  |

---

## Sample Output

```json
{
  "predicted_price": 452300.78,
  "currency": "USD"
}
```

---

## Deployment

This app is deployed using two free cloud services:

| Service          | Hosts        | URL                              |
| ---------------- | ------------ | -------------------------------- |
| Render           | FastAPI API  | `https://ca-house-api.onrender.com` |
| Streamlit Cloud  | Frontend     | `https://your-app.streamlit.app` |

### Steps

1. Push repo to GitHub (use Git LFS for the `.pkl` file if it exceeds 100MB)
2. Deploy `api.py` as a Web Service on [Render](https://render.com)
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
3. Deploy `app.py` on [Streamlit Cloud](https://share.streamlit.io)
   - Set secret: `API_URL = "https://ca-house-api.onrender.com"`

---

## Key Learning Outcomes

This project demonstrates:
* End-to-end ML pipeline development
* Model serving with FastAPI
* Streamlit UI engineering
* Feature validation
* Full-stack ML deployment workflow

---

## Future Improvements

Ordered by complexity:

* [ ] SHAP explainability for feature importance
* [ ] Model comparison dashboard (Random Forest vs XGBoost vs Linear)
* [ ] Prediction export as PDF report
* [ ] Docker containerization
* [ ] User authentication
* [ ] CI/CD pipeline with GitHub Actions

---

## Author

**Hamza Uzzaman**
Computer Science Student · Machine Learning & AI

---

## License

MIT License
Note:
.pkl is not there in the repo since its a large file and could not be uploaded you can access the file by running the .ipynb file completely
thanks
