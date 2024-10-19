# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8501 for Streamlit
EXPOSE 8501

# Set environment variables (replace with actual values or use .env files)
ENV PINECONE_API_KEY=your_pinecone_api_key
ENV HUGGINGFACE_API_KEY=your_huggingface_api_key

# Run Streamlit app
CMD ["streamlit", "run", "frontEnd.py"]

