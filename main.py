from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import car_sales

app = FastAPI(
    title="Car Sales Binary Tree API",
    description="API for managing car sales using a binary search tree",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@carsalesapi.com"
    },
    license_info={
        "name": "MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(car_sales.router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Car Sales Binary Tree API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
