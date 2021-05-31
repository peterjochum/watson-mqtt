FROM python:3.9

# Switch to working directory
WORKDIR /app

# Copy runtime requirements
COPY requirements.txt .

# Install runtime dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY *.py ./

# Disable python print output buffering
ENV PYTHONUNBUFFERED=1

# Entrypoint runs the main application
ENTRYPOINT ["python", "main.py"]
