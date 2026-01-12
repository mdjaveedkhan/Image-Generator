# Use Python 3.10
FROM python:3.10-slim

# Set up a home for our app
WORKDIR /app

# Install system dependencies for images
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
# We use the CPU version of torch to save space on the free tier
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Hugging Face Spaces run on port 7860
EXPOSE 7860

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
