# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only Python files to the working directory
COPY src/*.py ./

# Set the command to run the application
CMD ["python", "main.py"]
