from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Base + engine for DB creation
from app.db.database import engine, Base

# Routers
from app.routers import auth as auth_router
from app.routers import users as users_router

app = FastAPI(title="FastAPI JWT Role-Based Auth Project")

# CORS (Frontend can access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # put frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth_router.router)
app.include_router(users_router.router)


# Create DB tables on startup (for initial development)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"message": "FastAPI JWT Role-Based Backend Running"}
