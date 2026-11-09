FROM python:3.14-slim

WORKDIR /app

# Install libraries (CPU-only PyTorch keeps the image much smaller)
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Copy the code
COPY app ./app
COPY evals ./evals

# Build the knowledge base inside the image
RUN python app/ingest.py && python app/embed.py

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]