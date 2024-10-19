## Project Overview:
This project extends the capabilities of the chatbot by integrating a frontend interface using Streamlit for user interaction. It allows users to upload documents (PDF, text, or Word files), which the chatbot processes and uses to answer user queries. The chatbot uses Pinecone for document retrieval and Hugging Face's models for generating concise and relevant responses based on uploaded content.

## Key Features:
1. Ability to upload documents (PDF, Word, and text).
2. Uses Pinecone for document retrieval.
3. Hugging Face’s LLM for generative responses.

## Technologies Used:
1. Streamlit for the frontend.
2. Langchain for document processing and LLM integration.
3. Pinecone for vector storage.
4. Hugging Face for the language model.

## Package Requirement:

langchain
pinecone-client
langchain-community
sentence-transformers
Streamlit
PyPDF2
python-docx

Note: Ensure you have active API keys from both Hugging Face and Pinecone to use this application.

## Deployment 

### Option 1: Build from Source

1. Clone the repository:
    ```bash
    git clone https://github.com/Coderandme/Chat_Bot.git
    cd chat_Bot
    ```

### Option 2: Pull Pre-built Docker Image

If you prefer to use the pre-built Docker image, you can pull it directly from Docker Hub:

1. Pull the Docker image:
    ```bash
    docker pull bijeeta/chat_bot:Chat_Bot 
    ```

2. Run the Docker container:
    ```bash
    docker run -p 8501:8501 bijeeta/chat_bot:Chat_Bot
    ```

3. Access the application in the browser at `http://localhost:8501`.
