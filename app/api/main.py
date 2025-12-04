"""
Main FastAPI Application
Run with: uvicorn app.api.main:app --reload --port 8001
"""
from fastapi import FastAPI, HTTPException, Query, Path, Security, Depends
from fastapi.security.api_key import APIKeyHeader
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
from src.auth import validate_api_key

# Initialize settings
settings = get_settings()

# API Key Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Validate API Key"""
    key_data = validate_api_key(api_key_header)
    if not key_data:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials. Invalid or inactive API Key."
        )
    return key_data

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    **COVID-19 Vaccine Tracker REST API**
    
    This experimental API provides programmatic access to vaccination data, 
    forecasting, and AI chatbot features.
    
    ## Authentication
    
    **Requires API Key**: All endpoints require a valid `X-API-Key` header.
    
    ## Features
    
    * [Data] **Vaccination Data**: Get real-time stats for any country
    * [Forecast] **Forecasting**: ML-based predictions for future trends
    * [Bot] **AI Chatbot**: Natural language health assistant
    * [History] **Time Series**: Historical vaccination data
    
    ## Usage
    
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


# Root endpoint (Public)
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "message": "COVID-19 Vaccine Tracker API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "api_prefix": settings.api_prefix,
        "auth_required": True
    }


# Health check endpoint (Public)
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat()
    }


# Include routers with Security Dependency
app.include_router(
    vaccination.router,
    prefix=settings.api_prefix,
    tags=["Vaccination Data"],
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    forecast.router,
    prefix=settings.api_prefix,
    tags=["Forecasting"],
    dependencies=[Depends(get_api_key)]
)

app.include_router(
    chatbot.router,
    prefix=settings.api_prefix,
    tags=["AI Chatbot"],
    dependencies=[Depends(get_api_key)]
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
