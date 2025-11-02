Okay, I've updated the README to reflect that LM Studio is used instead of Ollama.

# PPT Maker - Agentic AI

Convert PDF or text files into professional PowerPoint presentations using a local Large Language Model (LLM) and intelligent content processing.
## Generated Files

**Generated PowerPoint files are saved in the `static/uploads/` directory.**
## Table of Contents

*   [Features](#features)
*   [Prerequisites](#prerequisites)
*   [Installation](#installation)
*   [Setting up the Local LLM (LM Studio)](#setting-up-the-local-llm-lm-studio)
*   [Usage](#usage)
*   [Project Structure](#project-structure)
*   [Generated Files](#generated-files)
*   [Logging](#logging)
*   [Troubleshooting](#troubleshooting)

## Features

*   **Agentic AI Processing:** Leverages a local LLM (Llama-3.2-3B) for intelligent content analysis.
*   **Document Conversion:** Converts PDF and TXT files into PowerPoint (PPTX) format.
*   **Content Refinement:** Uses AI to extract key sentences, identify headings, and refine content for presentations.
*   **Automatic Formatting:** Generates slides with professional layouts, varied colors, and clear structure.
*   **Modern UI:** Features a clean, modern Streamlit interface for easy interaction.
*   **Prompt Logging:** Records all prompts sent to the LLM and its responses for debugging and analysis.

## Prerequisites

*   Python 3.8 or higher
*   A local instance of the Llama-3.2-3B-Instruct model running at `http://127.0.0.1:1234` (e.g., using LM Studio)
*   (Optional but recommended) spaCy English model: `en_core_web_sm`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK Data:**
    *   Start a Python interpreter:
        ```bash
        python
        ```
    *   Run the NLTK downloader:
        ```python
        import nltk
        nltk.download('punkt_tab')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        exit()
        ```

5.  **Install spaCy model (optional but recommended for better NLP fallback):**
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Setting up the Local LLM (LM Studio)

This project requires a local LLM server compatible with the OpenAI API format, running at `http://127.0.0.1:1234`.

*   **Using LM Studio:**
    1.  Install LM Studio from [https://lmstudio.ai](https://lmstudio.ai).
    2.  Download the `Llama-3.2-3B-Instruct` model (or a compatible model) within LM Studio.
    3.  Load the model.
    4.  In the bottom-left corner, click the "Settings" icon (gear icon).
    5.  Go to the "Server" tab.
    6.  Click "Start Server". The server should start listening at `http://127.0.0.1:1234` by default.
    7.  Keep LM Studio running with the server active.

## Usage

1.  **Set the System Prompt:** Ensure your local LLM server (LM Studio) is configured with the following system prompt:
    ```
    You are an expert content analyzer and presentation creator. Your role is to process text content and generate structured, professional presentation slides. When given text content, you should:

    1. Extract the most important information concisely
    2. Create clear, impactful bullet points for slides
    3. Generate appropriate slide titles that summarize the content
    4. Maintain the original meaning while making it suitable for presentation format
    5. Respond directly to the request without unnecessary explanations like "I'd be happy to help..."
    6. Always return content in the requested format (e.g., one item per line for lists)
    7. Focus on key concepts, facts, and actionable information
    8. For slide titles, provide concise, descriptive headings that capture the main theme
    9. For content refinement, make text more concise and impactful while preserving meaning
    10. When extracting key sentences, return only the sentences, one per line, without numbering or additional text
    ```

2.  **Start the Flask Backend:**
    ```bash
    python backend.py
    ```
    The backend server will start on `http://localhost:5000`.

3.  **Start the Streamlit Frontend:**
    In a new terminal (with the same virtual environment activated):
    ```bash
    streamlit run app.py
    ```
    The Streamlit UI will open in your default browser.

4.  **Use the Application:**
    *   Upload a PDF or TXT file using the Streamlit interface.
    *   Click the "Generate Presentation" button.
    *   Wait for the processing to complete.
    *   Click the "Download Presentation" button to get your PPTX file.

## Project Structure

```
ppt-maker/
├── app.py                  # Streamlit frontend UI
├── backend.py              # Flask backend API
├── content_processor.py    # Core logic for content analysis using LLM
├── ppt_generator.py        # Logic for creating PowerPoint files
├── logging_backend.py      # Logging functionality for LLM prompts/responses
├── test_logging.py         # Simple script to test logging
├── requirements.txt        # Python dependencies
└── static/
    └── uploads/            # Directory for temporary file storage and generated PPTs
└── logs/                   # Directory for prompt/response logs
```

## Logging

Prompt and response logs are saved in the `logs/` directory:
*   `logs/prompt_response_log_<date>.log`: Human-readable log file.
*   `logs/interactions_<date>.jsonl`: JSON Lines file for programmatic access.

## Troubleshooting

*   **"Resource not found" errors (like `punkt_tab`):** Ensure you have run the `nltk.download()` commands as described in the Installation section.
*   **"Cannot connect to backend":** Verify that the Flask server (`backend.py`) is running on `http://localhost:5000`.
*   **"I'd be happy to help..." in PPT:** Ensure the system prompt is correctly set in your local LLM server (LM Studio).
*   **LLM not responding:** Check that your local LLM server (LM Studio) is running and accessible at `http://127.0.0.1:1234`.
