FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=booking_api.py  
ENTRYPOINT ["sh", "-c", "python init_db.py && flask run --host=0.0.0.0 --port=5000"]