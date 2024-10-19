import os
import pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone as PineconeVectorStore
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from pinecone import ServerlessSpec, Pinecone, PineconeApiException
from langchain.schema import Document  


class ChatBot:
    def __init__(self):
        self.api_key = 'Pinecone_API'  # Replace with your actual API key
        self.index_name = "langchain-demo"
        self.embeddings = HuggingFaceEmbeddings()

        # Set the PINECONE_API_KEY environment variable
        os.environ['PINECONE_API_KEY'] = self.api_key
        self.pc = Pinecone(api_key=self.api_key)  # Create a Pinecone instance

        # Check if index exists and delete if it does
        if self.index_name in self.pc.list_indexes().names():
            self.pc.delete_index(self.index_name)

        # Create a new index
        self.pc.create_index(
            name=self.index_name,
            dimension=768,  # Make sure this matches your embeddings
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws',        # Specify the cloud provider
                region='us-east-1'  # Specify the region
            )
        )

        # Initialize the documents with makeup.txt by default
        self.docsearch = self.load_makeup_file()

        self.llm = self.setup_llm()
         # Set up the RAG chain
        self.prompt_template = """
                You are a document assistant. Your main task is to help people find answers to questions based on the documents they upload.
                If you don't know the answer, simply say you don't know. Keep the answer concise and relevant to the question, ideally within 3 sentences.

                Context: {context}
                Question: {question}
                Answer:
            """

        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])

    def setup_llm(self):
        repo_id = 'mistralai/Mistral-7B-Instruct-v0.2'  # Replace with your model ID
        return HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=0.8,
            top_k=50,
            huggingfacehub_api_token='huggingface_API'  # Ensure this environment variable is set
        )

    def load_makeup_file(self):
        # Load and split the makeup.txt file
        loader = TextLoader('./makeup.txt', encoding='UTF-8')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=4)
        docs = text_splitter.split_documents(documents)
        # Store embedded segments in Pinecone
        docsearch = PineconeVectorStore.from_documents(docs, self.embeddings, index_name=self.index_name)
        return docsearch


    def process_uploaded_content(self, content):
        # Convert the content (string) into a list of Document objects
        doc = Document(page_content=content)
        # Now split the document into smaller chunks
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=4)
        docs = text_splitter.split_documents([doc])  # Use the Document object

        # Store embedded segments in Pinecone, replacing the previous docsearch
        self.docsearch = PineconeVectorStore.from_documents(docs, self.embeddings, index_name=self.index_name)

   

    def generate_response(self, input_text):
        # Ensure docsearch is available
        if self.docsearch is None:
            return "No documents uploaded or processed."
        rag_chain = (
            {"context": self.docsearch.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        result = rag_chain.invoke(input_text)
        return result


# # Outside ChatBot() class
# bot = ChatBot()
# user_input = input("Ask me anything: ")
# result = bot.rag_chain.invoke(user_input)
# print(result)

