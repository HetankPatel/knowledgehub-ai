from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="KnowledgeHub AI")

# Make files inside the "static" folder available to the browser.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    """Show the main webpage."""
    return FileResponse("static/index.html")


@app.get("/api/status")
def status():
    """Simple endpoint used to check that the backend is running."""
    return {"message": "KnowledgeHub AI is running"}
