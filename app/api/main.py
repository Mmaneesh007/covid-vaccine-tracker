"""
Main FastAPI Application
Run with: uvicorn app.api.main:app --reload --port 8001
"""
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.api.config import get_settings
from app.api.models import (
    VaccinationStats,
    TimeSeriesData,
    ForecastResponse,
    ChatRequest,
    ChatResponse,
    CountryListResponse,
    HealthResponse,
    ErrorResponse
)
from app.api.routes import vaccination, forecast, chatbot

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    **COVID-19 Vaccine Tracker REST API**
    
    This experimental API provides programmatic access to vaccination data, 
    forecasting, and AI chatbot features.
    
    ## Features
    
    * [Data] **Vaccination Data**: Get real-time stats for any country
    * [Forecast] **Forecasting**: ML-based predictions for future trends
    * [Bot] **AI Chatbot**: Natural language health assistant
    * [History] **Time Series**: Historical vaccination data
    
    ## Usage
    
    All endpoints return JSON responses. Authentication is not required for this experimental version.
    
    **Base URL**: `http://localhost:8001`
    
    **API Prefix**: `/api/v1`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "COVID-19 Vaccine Tracker API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "api_prefix": settings.api_prefix
    }


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat()
    }


# Include routers
app.include_router(
    vaccination.router,
    prefix=settings.api_prefix,
    tags=["Vaccination Data"]
)

app.include_router(
    forecast.router,
    prefix=settings.api_prefix,
    tags=["Forecasting"]
)

app.include_router(
    chatbot.router,
    prefix=settings.api_prefix,
    tags=["AI Chatbot"]
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "status_code": 500
        }
    )


# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "detail": f"The endpoint {request.url.path} does not exist",
            "status_code": 404
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
