# 1. Use an official Python base image
FROM python:3

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy dependency files first for caching
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the full application code
COPY . .

# 6. Expose the port FastAPI will run on
EXPOSE 8000

# 7. Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
