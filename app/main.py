from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import user, franchise
from app.routes.auth import router as auth_router
from app.routes.franchise import router as franchise_router
from app.routes.profile import router as profile_router
from app.routes.websocket import router as websocket_router

app = FastAPI(title="Franchise Management System")


@app.get("/")
def root():
    return {"message": "Project is working"}


@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database Connected Successfully")
    except Exception as e:
        print("❌ Database Connection Failed:", e)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(franchise_router, prefix="/api/v1/franchise", tags=["Franchise"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(websocket_router, prefix="/ws", tags=["WebSocket"])