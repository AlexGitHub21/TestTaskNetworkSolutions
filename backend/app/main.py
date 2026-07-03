from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app import apps_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(router=apps_router)


def start():
    uvicorn.run(app="app.main:app", reload=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)