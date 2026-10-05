import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.gemma_api import router as gemma_router
from app.llama_api import router as llama_router
from app.whisper_api import router as whisper_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gemma_router)
app.include_router(llama_router)
app.include_router(whisper_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}




if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000)