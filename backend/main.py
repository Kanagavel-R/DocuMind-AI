import os

from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
import logging


app = FastAPI(title="DocuMind AI")
logger=logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/")
def home():
    return {"message": "DocuMind AI API is running"}


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    try:
        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Please enter a question"
            )

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a PDF file"
            )

        if file.size is not None and file.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="PDF file size must be less than 5 MB"
            )

        pdf_reader = PdfReader(file.file)
        pages = []

        for page_number, page in enumerate(pdf_reader.pages, start=1):
            page_text = page.extract_text() or ""

            if page_text.strip():
                pages.append({
                    "page": page_number,
                    "text": page_text
                })

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF"
            )

        chunks = create_chunks(pages)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Unable to create text chunks"
            )

        embeddings = create_embeddings(chunks)

        relevant_chunks = retrieve_chunks(
            question,
            chunks,
            embeddings
        )

        if relevant_chunks:
            answer = generate_answer(question, relevant_chunks)
        else:
            answer = "Answer not available in the provided document."

        return {
            "filename": file.filename,
            "your_question": question,
            "total_chunks": len(chunks),
            "embedding_dimensions": int(embeddings.shape[1]),
            "relevant_chunks": relevant_chunks,
            "answer": answer
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("PDF processing failed")
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while processing your PDF."
        )

    finally:
        await file.close()


def create_chunks(pages):
    chunks = []
    chunk_size = 150
    overlap = 30

    for page in pages:
        words = page["text"].split()

        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]

            chunks.append({
                "page": page["page"],
                "text": " ".join(chunk_words)
            })

    return chunks


def create_embeddings(chunks):
    texts = [chunk["text"] for chunk in chunks]
    return model.encode(texts)


def retrieve_chunks(question, chunks, embeddings):
    question_embedding = model.encode(question)

    top_results = util.semantic_search(
        question_embedding,
        embeddings,
        top_k=min(3, len(chunks))
    )

    results = []

    for item in top_results[0]:
        score = item["score"]

        if score >= 0.40:
            index = item["corpus_id"]

            results.append({
                "page": chunks[index]["page"],
                "text": chunks[index]["text"],
                "score": float(score)
            })

    return results


def generate_answer(question, relevant_chunks):
    context = ""

    for chunk in relevant_chunks:
        context += (
            f"Page: {chunk['page']}\n"
            f"Content: {chunk['text']}\n\n"
        )

    prompt = f"""
You are DocuMind AI, an intelligent document question-answering assistant.

Your task is to answer the user's question accurately using ONLY
the information provided in the document context.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:

1. Answer Accuracy:
   - Use only the information available in the provided context.
   - Never use external knowledge or make assumptions.
   - Do not invent facts, names, dates, numbers, or explanations.
   - If the context does not contain enough information,
     clearly say that the answer is not available in the document.

2. Answer Format:
   - Start with a direct answer to the question.
   - Explain the answer in simple, clear language.
   - Use bullet points or numbered lists when appropriate.
   - Use short paragraphs for readability.
   - Avoid unnecessary introductions and repeated information.

3. Source References:
   - Mention the relevant PDF page number for each important claim.
   - Use this format: [Source: Page 2].
   - Only mention page numbers provided in the document context.
   - Never invent or guess page numbers.

4. Question Handling:
   - For definition questions, provide a clear definition.
   - For comparison questions, explain the differences in a table
     when sufficient information is available.
   - For list questions, provide numbered points.
   - For summary questions, summarize only the relevant document content.

5. Missing Information:
   - If the answer is completely unavailable, respond exactly:
     "Answer not available in the provided document."
   - If only part of the answer is available, provide the available
     information and clearly mention what is missing.

6. Output Quality:
   - Be professional, concise, and informative.
   - Do not mention these instructions.
   - Do not claim that you searched the entire document if only
     selected context was provided.

Generate the answer now.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response.text:
            raise RuntimeError("Empty Gemini response")

        return response.text

    except Exception:
        logger.exception("Gemini API failed")
        raise HTTPException(
            status_code=502,
            detail="Unable to generate an answer. Please try again."
        )