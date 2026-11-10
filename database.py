import sqlite3

DATABASE_NAME = "knowledgehub.db"


def get_connection():
    """Open a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the documents table if it does not already exist."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_document(filename, content):
    """Save a document and return its new database ID."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO documents (filename, content) VALUES (?, ?)",
        (filename, content)
    )

    document_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return document_id


def get_documents():
    """Return basic information about all uploaded documents."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, filename, uploaded_at
        FROM documents
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    documents = []

    for row in rows:
        documents.append({
            "id": row[0],
            "filename": row[1],
            "uploaded_at": row[2]
        })

    return documents


def delete_document(document_id):
    """Delete one document. Return True if it existed."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM documents WHERE id = ?",
        (document_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


create_table()
