from ai_tools import (
    answer_question,
    find_best_chunk,
    split_text
)


def test_split_text_creates_chunks():

    text = " ".join(
        ["word"] * 250
    )

    chunks = split_text(
        text,
        chunk_size=100
    )

    assert len(chunks) == 3


def test_find_best_chunk_finds_relevant_document():

    documents = [
        {
            "filename": "python.txt",
            "content":
                "The application uses Python and FastAPI "
                "for backend development."
        },
        {
            "filename": "gardening.txt",
            "content":
                "Tomatoes grow well with sunlight "
                "and regular watering."
        }
    ]

    result = find_best_chunk(
        "Which document talks about Python and FastAPI?",
        documents
    )

    assert result is not None

    assert result["filename"] == "python.txt"


def test_find_best_chunk_with_no_documents():

    result = find_best_chunk(
        "What is Python?",
        []
    )

    assert result is None


def test_answer_question_with_no_documents():

    result = answer_question(
        "What database is used?",
        []
    )

    assert result["answer"] == \
        "No document content was found."

    assert result["source"] is None
