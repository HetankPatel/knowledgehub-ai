from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader

import database


app = FastAPI(title="KnowledgeHub AI")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    """Show the main webpage."""
    return FileResponse("static/index.html")


@app.get("/api/status")
def status():
    """Check that the backend is running."""
    return {"message": "KnowledgeHub AI is running"}


def extract_text(filename, file_bytes):
    """Extract text from a TXT, Markdown, or PDF file."""

    extension = Path(filename).suffix.lower()

    if extension in [".txt", ".md"]:
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="The text file could not be read."
            )

    if extension == ".pdf":
        try:
            reader = PdfReader(BytesIO(file_bytes))
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="The PDF could not be read."
            )

    raise HTTPException(
        status_code=400,
        detail="Only TXT, MD, and PDF files are supported."
    )


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and save its text in SQLite."""

    file_bytes = await file.read()

    text = extract_text(file.filename, file_bytes)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="The document does not contain readable text."
        )

    document_id = database.add_document(
        file.filename,
        text
    )

    return {
        "message": "Document uploaded successfully.",
        "id": document_id,
        "filename": file.filename
    }


@app.get("/api/documents")
def list_documents():
    """Return all uploaded documents."""
    return database.get_documents()


@app.delete("/api/documents/{document_id}")
def remove_document(document_id: int):
    """Delete one uploaded document."""

    deleted = database.delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {"message": "Document deleted successfully."}
