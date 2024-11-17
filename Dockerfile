# Use the official Python image as a base
FROM python:3.10-slim

# Set up the working directory inside the container
WORKDIR /app

# Copy the contents of your local directory to the /app directory in the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Streamlit to listen on port 8080, required by Cloud Run
ENV PORT 8080

# Expose the port Cloud Run will use
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "my_app.py", "--server.port=8080", "--server.enableCORS=false"]
