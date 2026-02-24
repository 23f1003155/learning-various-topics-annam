# Use official Python image as base
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file into container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy your app code into container
COPY main.py .

# Expose port 8000 (so outside world can access it)
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]