# InsightDocs AI: Chat with Your PDF

A powerful Streamlit application that allows you to upload PDF documents and chat with them using Retrieval-Augmented Generation (RAG) powered by Google's Gemini AI.

<img width="1899" height="921" alt="Screenshot 2026-02-04 123147" src="https://github.com/user-attachments/assets/5d08427a-14b9-4019-a412-c491d9e75c3e" />

## Features

- 📄 **PDF Upload & Processing**: Upload PDF documents and process them for analysis
- 🤖 **AI-Powered Chat**: Chat with your documents using Google's Gemini AI models
- 🔍 **Intelligent Retrieval**: Uses FAISS vector search for efficient document retrieval
- 🎨 **Modern UI**: Clean and intuitive Streamlit interface
- 🔒 **Secure API Key Management**: Secure input for your Gemini API key

## Prerequisites

- Python 3.8 or higher
- A valid Google Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd chat-pdf
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. In the sidebar:
   - Enter your Gemini API key
   - Upload a PDF document
   - Click "Process Document"

4. Start chatting with your PDF in the chat interface!

## Dependencies

- streamlit: Web app framework
- langchain: Framework for building LLM applications
- langchain-community: Community integrations for LangChain
- langchain-huggingface: HuggingFace integrations
- langchain-google-genai: Google Generative AI integration
- pypdf: PDF processing library
- sentence-transformers: Text embeddings
- faiss-cpu: Vector similarity search

## How It Works

1. **Document Processing**: PDFs are loaded and split into manageable chunks
2. **Embeddings**: Text chunks are converted to vector embeddings using HuggingFace models
3. **Vector Storage**: Embeddings are stored in a FAISS vector database
4. **Retrieval**: When you ask a question, relevant document chunks are retrieved
5. **Generation**: Gemini AI generates answers based on the retrieved context

## Configuration

- **Chunk Size**: 1000 characters with 200 character overlap
- **Embedding Model**: all-MiniLM-L6-v2 (fast and efficient)
- **Vector Store**: FAISS for local similarity search
- **LLM**: Google Gemini (configurable in the code)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application requires a valid Google Gemini API key. Usage costs may apply based on your API usage. Please refer to Google's pricing for more information.
