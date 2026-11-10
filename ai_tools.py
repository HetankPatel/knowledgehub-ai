from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline


qa_model = None


def split_text(text, chunk_size=120):
    """
    Split a long document into smaller groups of words.
    """

    words = text.split()

    chunks = []

    for start in range(0, len(words), chunk_size):

        end = start + chunk_size

        chunk = words[start:end]

        chunks.append(" ".join(chunk))

    return chunks


def find_best_chunk(question, documents):
    """
    Find the document section that is most related
    to the user's question.
    """

    chunks = []

    for document in documents:

        document_chunks = split_text(document["content"])

        for chunk in document_chunks:

            chunks.append({
                "filename": document["filename"],
                "text": chunk
            })


    if len(chunks) == 0:
        return None


    texts = [question]

    for chunk in chunks:
        texts.append(chunk["text"])


    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(texts)


    question_vector = vectors[0]

    chunk_vectors = vectors[1:]


    scores = cosine_similarity(
        question_vector,
        chunk_vectors
    )[0]


    best_index = scores.argmax()

    best_chunk = chunks[best_index]

    best_chunk["similarity"] = float(scores[best_index])

    return best_chunk


def get_qa_model():
    """
    Load the question-answering model only when
    it is needed for the first time.
    """

    global qa_model

    if qa_model is None:

        qa_model = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad"
        )

    return qa_model


def answer_question(question, documents):
    """
    Find the best document section and use the
    AI model to answer the question from it.
    """

    best_chunk = find_best_chunk(
        question,
        documents
    )


    if best_chunk is None:

        return {
            "answer": "No document content was found.",
            "source": None,
            "similarity": 0
        }


    if best_chunk["similarity"] < 0.05:

        return {
            "answer": "I could not find enough relevant information in the uploaded documents.",
            "source": None,
            "similarity": best_chunk["similarity"]
        }


    model = get_qa_model()


    result = model(
        question=question,
        context=best_chunk["text"]
    )


    return {
        "answer": result["answer"],
        "source": best_chunk["filename"],
        "similarity": best_chunk["similarity"],
        "confidence": float(result["score"])
    }
