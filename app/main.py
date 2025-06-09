from fastapi import FastAPI, Header, HTTPException, Request
from dotenv import load_dotenv
from starlette.responses import JSONResponse
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("FASTAPI_KEY")

@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exc:
        # FastAPI HTTP-Error → JSON-Response without Stacktrace
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as exc:
        # All other errors
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/users/{user_id}")
def get_user(user_id: int, x_api_key: str = Header(None)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server not properly configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {"id": user_id, "name": f"User {user_id}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}