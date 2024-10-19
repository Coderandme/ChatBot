import streamlit as st
import PyPDF2
import docx
from backEnd import ChatBot  # Assuming ChatBot is defined in backEnd.py

st.set_page_config(page_title="Chat Bot")
with st.sidebar:
    st.title('Assistant')

# Initialize the chatbot only once and store it in session_state
if 'bot' not in st.session_state:
    st.session_state['bot'] = ChatBot()  # Ensure the chatbot is initialized once

# Store uploaded documents in session state
if 'uploaded_documents' not in st.session_state:
    st.session_state['uploaded_documents'] = []

# Store the filename of the last uploaded file to avoid reprocessing
if 'last_uploaded_file' not in st.session_state:
    st.session_state['last_uploaded_file'] = None

# Function for generating LLM response
def generate_response(input_text):
    result = st.session_state['bot'].generate_response(input_text)
    return result

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, let me know how I can help you"}]

# Maximum file size limit in MB
MAX_FILE_SIZE_MB = 5

# File upload functionality
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx"])

# Process the file only if it is newly uploaded
if uploaded_file is not None and uploaded_file != st.session_state['last_uploaded_file']:
    # Check the file size
    file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert size to MB
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB. Please upload a smaller file.")
    else:
        content = uploaded_file.read()

        # Process the content based on the file type
        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
        elif uploaded_file.type == "text/plain":
            content = content.decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            content = "\n".join([para.text for para in doc.paragraphs])

        # Pass the content to the backend for processing
        st.session_state['bot'].process_uploaded_content(content)
        st.session_state['uploaded_documents'].append(content)  # Store uploaded content
        st.session_state['last_uploaded_file'] = uploaded_file  # Remember the last uploaded file

        st.session_state.messages.append({"role": "assistant", "content": "Document uploaded and processed successfully."})

# Display uploaded documents
if st.session_state['uploaded_documents']:
    st.subheader("Uploaded Documents:")
    for i, doc in enumerate(st.session_state['uploaded_documents']):
        st.write(f"Document {i + 1}:")
        st.write(doc[:100] + "...")  # Display a snippet of the document (first 100 characters)


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from my experience..."):
            response = generate_response(input)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)


