FROM python:3.12-slim

# Git is needed to install the git-based dependency in requirements.txt
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Store all application files in /api
WORKDIR /api

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Indicate that the container should listen on port 8000
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]