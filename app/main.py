from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur SkillFlow API 🚀"}




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les sources
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
