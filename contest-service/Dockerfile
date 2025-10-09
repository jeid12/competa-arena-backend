# Stage 1: Build
FROM maven:3.9.0-eclipse-temurin-17 AS build

WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run
FROM eclipse-temurin:17-jre

WORKDIR /app

COPY --from=build /app/target/contest-service-0.0.1-SNAPSHOT.jar ./contest-service.jar

# Expose port
EXPOSE 8080

# Run jar
ENTRYPOINT ["java", "-jar", "contest-service.jar"]
