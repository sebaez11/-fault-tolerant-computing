# Dockerizing a Django Project with Docker Compose

In this tutorial, we'll walk through the process of setting up a Django project with Docker and Docker Compose. Docker is a containerization platform that allows you to package your application and its dependencies into a single unit called a container.

## Technologies Used

- **Django**: A high-level Python web framework.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **Docker Compose**: A tool for defining and running multi-container Docker applications.

## Project Structure

Before we dive into the Docker setup, let's understand the structure of our Django project.

```
dentaloffice/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
│
└── ...
```

- **Dockerfile**: This file contains instructions for building a Docker image for our Django project.
- **docker-compose.yml**: This file defines the services, networks, and volumes for our Docker application.
- **requirements.txt**: Lists Python packages and dependencies for our Django application.

## Dockerfile

The Dockerfile is used to create a Docker image for our Django application. It specifies the base image, environment variables, and the necessary commands to set up the environment.

```dockerfile
# Use the official Python 3.9 base image
FROM python:3.9

# Prevent the generation of .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Copy and install project dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose port 8000 for the Django server
EXPOSE 8000

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

- `FROM python:3.9`: We use the official Python 3.9 base image.
- `ENV`: Set environment variables to configure Python's behavior.
- `RUN`: Create a working directory and install project dependencies.
- `COPY`: Copy your project code into the container.
- `EXPOSE`: Expose port 8000 for the Django server.
- `CMD`: Start the Django application using the `manage.py runserver` command.

## docker-compose.yml

The docker-compose.yml file defines how our multi-container application should behave. It includes services, network configuration, and volume mounting.

```yaml
version: '3'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: dental_db
      POSTGRES_USER: dental_user
      POSTGRES_PASSWORD: dental_password
```

- `services`: We define two services, "web" for our Django application and "db" for the PostgreSQL database.
- `build`: Specify the build context and the Dockerfile to use.
- `volumes`: Mount the current directory into the container at `/app`.
- `ports`: Map port 8000 from the container to the host.
- `depends_on`: Ensure that the "web" service starts after the "db" service is up.

## Running the Application

1. Make sure you have Docker and Docker Compose installed.

2. Open a terminal and navigate to your project root directory.

3. Build and start the application:

   ```bash
   docker-compose up --build
   ```

4. Access your Django application in a web browser at http://localhost:8000.

## Results

![Docker console](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaCyzFaH-vJI2UDeaVqyRNOiUwocuq9c4TSvdwwfmiPh2V52-6888CC5bwnmH8n91TDF79jYCpHSZAaGTgrTNMs7NBfjkw=w1920-h1080)  
![Django admin](https://lh3.googleusercontent.com/u/2/drive-viewer/AK7aPaAbQOsY9Es5YkjuT1DVrlhe-T_Dh1Rz_Re0a3WymyVdaUa2DSpe-L-NloO2kIQT2Lf2OGDC6njgLs4zlhN_NYGWDbGp=w1920-h1080)

Now you have a Dockerized Django project up and running! This setup makes it easy to share and deploy your application across different environments.

This tutorial provides a basic introduction to Docker and Docker Compose for Django. You can further customize and expand your setup to suit your specific project needs.

Happy coding!
