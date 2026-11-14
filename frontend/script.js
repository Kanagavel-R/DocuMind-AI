
const form = document.querySelector("form");

const pdfInput = document.getElementById("pdf");
const questionInput = document.getElementById("question");
const result = document.getElementById("result");

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const pdfFile = pdfInput.files[0];
    const question = questionInput.value.trim();

    // Validate inputs
    if (!pdfFile) {
        result.textContent = "Please upload a PDF!";
        return;
    }

    if (!question) {
        result.textContent = "Please enter a question!";
        return;
    }

    // Prepare form data
    const formData = new FormData();

    formData.append("file", pdfFile);
    formData.append("question", question);

    try {

        result.textContent = "Processing your PDF... Please wait.";

        // Send request to FastAPI
        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        result.replaceChildren();

// Answer section
const answerCard = document.createElement("div");
answerCard.className = "answer-card";

const answerTitle = document.createElement("h2");
answerTitle.textContent = "AI Generated Answer";

const answerText = document.createElement("p");
answerText.textContent = data.answer;

answerCard.append(answerTitle, answerText);
result.appendChild(answerCard);

// Relevant chunks section
const chunksCard = document.createElement("div");
chunksCard.className = "chunks-card";

const chunksTitle = document.createElement("h2");
chunksTitle.textContent = "Relevant Sources";

chunksCard.appendChild(chunksTitle);

data.relevant_chunks.forEach((chunk, index) => {

    const chunkItem = document.createElement("div");
    chunkItem.className = "chunk-item";

    const heading = document.createElement("h3");
    heading.textContent = `Source ${index + 1}`;

    const pageInfo = document.createElement("h4");
    pageInfo.textContent = `Page: ${chunk.page}`;

    const paragraph = document.createElement("p");
    paragraph.textContent = chunk.text;

    chunkItem.append(heading, pageInfo, paragraph);

    chunksCard.appendChild(chunkItem);
});

result.appendChild(chunksCard);
    } catch (error) {

        result.textContent = "Error: " + error.message;

    }

});
