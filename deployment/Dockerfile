FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for git and analysis tools
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType=none"]
