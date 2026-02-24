"""
API v1 роутерлари
"""
from fastapi import APIRouter
from app.api.v1 import auth, locations, employees, analytics, cameras, integrations

api_router = APIRouter()

# Роутерларини улаш
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(employees.router, prefix="/employees", tags=["Employees"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["Cameras"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["Integrations"])

