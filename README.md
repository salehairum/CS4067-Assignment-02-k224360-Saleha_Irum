# Online Event Booking System
## Tech Stacks
- User Service: FastAPI/PostgreSQL
- Event Service: Springboot/MongoDB
- Booking Service: Flask/PostgreSQL
- Notification Service: Flask/MongoDB
- Payment Service(mock): Flask
- Frontend: HTML, CSS, JS
- Communications: REST API(Sync), RabbitMQ(Async)

## API Documentation
- User Service: http://127.0.0.1:8000/docs
- Event Service: http://localhost:8080/swagger-ui/index.html
- Booking Service: http://127.0.0.1:5000/
- Notification Service: http://127.0.0.1:5001/

## Setup Guide
- Run user service using uvicorn main:app --reload
- Run event service using mvn spring-boot:run
- Run Booking service using python booking_api.py
- Run notification service using python notification_api.py
- Run consumer in notification service using python consumer.py
- Run payment service using python payment_api.py
- Start rabbitmq using net start rabbitmq

## Architecture
![image](https://github.com/user-attachments/assets/1668ee49-efb8-4cc5-bdc2-4a4a4065d138)

