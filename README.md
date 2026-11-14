📄 DocuMind AI

AI-Powered PDF Question Answering System using Retrieval-Augmented Generation (RAG)

DocuMind AI is an AI-powered document assistant that allows users to upload PDF documents and ask questions in natural language. It uses Retrieval-Augmented Generation (RAG), semantic search, and Google Gemini AI to generate context-aware answers based on the uploaded document.

The system also displays relevant source chunks, PDF page numbers, and similarity scores to help users understand where the answers come from.

🎥 Project Demo Video

▶️ "Watch DocuMind AI – Project Demonstration" (https://drive.google.com/file/d/1qv0shbJGw-2RaaCdhA8NstuQtOCT2aYn/view?usp=drivesdk)

✨ Features

- PDF Upload: Upload PDF documents through a simple web interface.
- PDF Text Extraction: Extract text from PDF documents using PyPDF.
- Text Chunking: Split extracted text into smaller chunks with overlapping content.
- Semantic Search: Retrieve relevant document chunks using Sentence Transformers.
- AI-Powered Answers: Generate context-aware answers using Google Gemini.
- Source References: Display relevant PDF page numbers.
- Similarity Scores: Show semantic similarity scores for retrieved chunks.
- Input Validation: Validate PDF files, file size, and user questions.
- Error Handling: Handle invalid files and AI API failures.

🛠️ Technology Stack

Layer| Technology
Frontend| HTML, CSS, JavaScript
Backend| Python, FastAPI
PDF Processing| PyPDF
Embeddings| Sentence Transformers
Embedding Model| all-MiniLM-L6-v2
Vector Retrieval| Semantic Search
AI Model| Google Gemini 2.5 Flash
API Testing| FastAPI Swagger UI
Version Control| Git and GitHub

🧠 How It Works

DocuMind AI follows a Retrieval-Augmented Generation (RAG) pipeline.

1. Upload: User uploads a PDF document.
2. Extract: Backend extracts text from the PDF.
3. Chunk: Extracted text is divided into smaller overlapping chunks.
4. Embed: Sentence Transformers converts text chunks into numerical embeddings.
5. Retrieve: Semantic search identifies the most relevant chunks for the user's question.
6. Generate: Retrieved context is sent to Google Gemini.
7. Answer: Gemini generates an answer using the provided document context.
8. Sources: The application displays relevant source chunks, page numbers, and similarity scores.

Architecture

              USER
                |
                v
         HTML / CSS / JS
                |
                v
          FastAPI Backend
                |
                v
           PDF Upload
                |
                v
          PDF Text Extraction
                |
                v
            Text Chunking
                |
                v
       Sentence Transformer
                |
                v
          Text Embeddings
                |
                v
          Semantic Search
                |
                v
        Relevant Text Chunks
                |
                v
        Google Gemini API
                |
                v
          AI Generated Answer
                |
                v
       Answer + Source References
                |
                v
          FRONTEND DISPLAY



## 📁 Project Structure

```text
DocuMind-AI/
│
├── index.html
├── style.css
├── script.js
│
├── backend/
│   ├── main.py
│   └── .gitignore
│
└── README.md

Note: The ".env" file contains the Gemini API key. It is stored locally and excluded from GitHub using ".gitignore".

⚙️ Installation and Setup

Prerequisites

- Python
- VS Code
- Git
- Google Gemini API Key

1. Clone the Repository

git clone https://github.com/Kanagavel-R/DocuMind-AI.git

cd DocuMind-AI

2. Set Up the Backend

cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required packages:

pip install fastapi uvicorn python-multipart python-dotenv google-genai pypdf sentence-transformers

3. Configure Environment Variables

Create a ".env" file inside the backend folder.

Add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key

Replace the placeholder with your own API key.

Never share or upload your API key.

4. Run the Backend

From the backend directory, run:

uvicorn main:app --reload

Backend API:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

5. Run the Frontend

Open the "frontend" folder in VS Code.

Use the Live Server extension to run "index.html".

The frontend communicates with the FastAPI backend.

🔌 API Endpoints

Method| Endpoint| Description
GET| "/"| Check backend status
POST| "/ask"| Upload PDF and ask a question
GET| "/docs"| Swagger API documentation

POST /ask

Request: Multipart form-data

Parameter| Type| Description
file| File| PDF document
question| String| User question

The API returns:

- Uploaded filename
- User question
- Total number of chunks
- Embedding dimensions
- Relevant source chunks
- PDF page numbers
- Similarity scores
- AI-generated answer

🔐 Security and Validation

- API keys are stored in environment variables.
- ".env" is excluded through ".gitignore".
- PDF file extension and signature are validated.
- PDF upload size is limited to 5 MB in the application.
- Empty questions are rejected.
- API errors are handled with appropriate HTTP responses.

🚀 Future Improvements

- OCR support for scanned PDFs.
- Support for multiple PDF documents.
- Persistent vector storage.
- User authentication and authorization.
- Improved retrieval accuracy and evaluation.
- Backend and frontend cloud deployment.

👨‍💻 Author

Kanagavel R.

B.Tech Information Technology

Chennai Institute of Technology

GitHub: "Kanagavel-R" (https://github.com/Kanagavel-R)

---

⭐ If you find this project interesting, feel free to explore the repository and watch the demo!