# Use a Python 3.10 image
FROM python:3.10-slim

# Set up a new user so we don't run as root
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /home/user/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the app
COPY --chown=user . .

# Expose the port HF expects
EXPOSE 7860

# Run the app with Gunicorn (Better for production)
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--timeout", "300", "app:app"]
