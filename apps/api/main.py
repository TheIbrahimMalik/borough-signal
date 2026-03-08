from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.graph import router as graph_router
from routes.lookups import router as lookups_router
from routes.runs import router as runs_router
from routes.simulate import router as simulate_router

app = FastAPI(title="BoroughSignal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lookups_router)
app.include_router(simulate_router)
app.include_router(runs_router)
app.include_router(graph_router)

@app.get("/health")
def health():
    return {"status": "ok"}
