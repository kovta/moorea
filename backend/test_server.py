from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI(title="Moorea Test Server")

@app.get("/")
async def root():
    return {"status": "working", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Test server is running"}

if __name__ == "__main__":
    print("🚀 Starting test server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
