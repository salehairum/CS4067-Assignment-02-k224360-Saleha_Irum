FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=payment_api.py  
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]