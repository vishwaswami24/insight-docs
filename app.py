import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# --- UI Configuration ---
st.set_page_config(page_title="InsightDocs AI", layout="wide")
st.title("📄 InsightDocs: Chat with your PDF")

# --- Sidebar for Uploads ---
with st.sidebar:
    st.header("Upload Center")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    process_button = st.button("Process Document")

    # API Key Input
    st.header("API Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    if api_key:
        st.session_state.api_key = api_key
        st.success("API Key set!")
    elif "api_key" not in st.session_state:
        st.warning("Please enter your Gemini API Key to use the chat feature.")

# --- RAG Logic ---
if uploaded_file and process_button:
    with st.spinner("Analyzing document..."):
        # 1. Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # 2. Load and Split
        loader = PyPDFLoader("temp.pdf")
        pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(pages)

        # 3. Create Embeddings & Vector Store
        # Using a small, fast model: all-MiniLM-L6-v2
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        
        # 4. Store in Session State
        st.session_state.vectorstore = vectorstore
        st.success("Analysis complete! Ask your questions below.")

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if "vectorstore" in st.session_state:
        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("Please enter your Gemini API Key in the sidebar to continue.")
            st.stop()

        # Initialize Gemini LLM
        llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=st.session_state.api_key, temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2)

        # Create a prompt template
        template = """Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Answer:"""
        qa_prompt = PromptTemplate.from_template(template)

        # Function to format documents
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Create the chain
        retriever = st.session_state.vectorstore.as_retriever()
        qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | qa_prompt
            | llm
            | StrOutputParser()
        )

        with st.chat_message("assistant"):
            response = qa_chain.invoke(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error("Please upload and process a PDF first!")