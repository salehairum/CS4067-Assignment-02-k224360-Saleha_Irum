FROM python:3.12-slim
WORKDIR /app    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]