FROM python:3.9-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${ML_PORT}

# Command to run the application
CMD ["python", "app.py"] 