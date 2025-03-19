FROM openjdk:23-jdk-slim
WORKDIR /app
COPY ./events_api/target/demo-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]