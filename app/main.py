from fastapi import FastAPI

app = FastAPI(title="Pramith Python API")

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
