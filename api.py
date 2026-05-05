import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CA House Price Predictor API",
    description="Serves a RandomForest sklearn pipeline trained on the California Housing dataset.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model loading ─────────────────────────────────────────────────────────────
_model = None
_model_error: str | None = None

try:
    from model_loader import load_model
    _model = load_model()
    logger.info("Model loaded successfully.")
except Exception as e:
    _model_error = str(e)
    logger.error(f"Model failed to load: {e}")


# ── Schemas ───────────────────────────────────────────────────────────────────
class HouseInput(BaseModel):
    longitude:          float
    latitude:           float
    housing_median_age: int
    total_rooms:        int
    total_bedrooms:     int
    population:         int
    households:         int
    median_income:      float
    ocean_proximity:    str

    model_config = {"json_schema_extra": {"example": {
        "longitude": -122.23, "latitude": 37.88, "housing_median_age": 41,
        "total_rooms": 880, "total_bedrooms": 129, "population": 322,
        "households": 126, "median_income": 8.3252, "ocean_proximity": "NEAR BAY",
    }}}


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "USD"


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "CA House Price Predictor API", "docs": "/docs"}


@app.get("/health")
def health():
    if _model is None:
        raise HTTPException(status_code=503, detail=f"Model not loaded: {_model_error}")
    return {"status": "ok", "model": "loaded"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: HouseInput):
    if _model is None:
        raise HTTPException(status_code=503, detail=f"Model not available: {_model_error}")

    # Field-level validation
    if data.total_rooms <= 0:
        raise HTTPException(status_code=400, detail="total_rooms must be > 0")
    if data.total_bedrooms <= 0:
        raise HTTPException(status_code=400, detail="total_bedrooms must be > 0")
    if data.population <= 0:
        raise HTTPException(status_code=400, detail="population must be > 0")
    if data.households <= 0:
        raise HTTPException(status_code=400, detail="households must be > 0")
    if data.median_income <= 0:
        raise HTTPException(status_code=400, detail="median_income must be > 0")

    # Cross-field validation
    if data.total_bedrooms > data.total_rooms:
        raise HTTPException(status_code=400, detail="total_bedrooms cannot exceed total_rooms")
    if data.households > data.population:
        raise HTTPException(status_code=400, detail="households cannot exceed population")

    valid_proximities = {"<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"}
    if data.ocean_proximity not in valid_proximities:
        raise HTTPException(status_code=400, detail=f"ocean_proximity must be one of {valid_proximities}")

    df = pd.DataFrame([data.model_dump()])
    prediction = float(_model.predict(df)[0])

    logger.info(
        f"Prediction: ${prediction:,.0f} | "
        f"loc=({data.latitude:.2f},{data.longitude:.2f}) | "
        f"ocean={data.ocean_proximity} | income={data.median_income}"
    )

    return PredictionResponse(predicted_price=round(prediction, 2))