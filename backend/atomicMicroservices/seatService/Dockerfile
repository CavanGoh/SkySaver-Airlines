# Step 1: Use an official Java runtime as a parent image
FROM openjdk:17-jdk-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the application's jar file to the container
# Assuming your Spring Boot application is built with Maven and the jar file is located in the target folder
COPY target/demo-0.0.1-SNAPSHOT.jar app.jar

# Step 4: Expose the port the app runs on
EXPOSE 8080

# Step 5: Define the command to run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
