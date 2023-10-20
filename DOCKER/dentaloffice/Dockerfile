# Usa la imagen base oficial de Python 3.9
FROM python:3.9

# Establece variables de entorno para evitar la generación de archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crea y establece el directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Copia el archivo requirements.txt e instala las dependencias
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia el contenido de tu proyecto al contenedor
COPY . /app/

# Expón el puerto 8000 para el servidor web de Django
EXPOSE 8000

# Inicia la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

