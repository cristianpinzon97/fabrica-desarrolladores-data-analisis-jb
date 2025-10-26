# Usa la imagen oficial de Python slim
FROM python:3.14-slim

# Establece el directorio de trabajo en src
WORKDIR /app/src

# Instala pipenv
RUN pip install pipenv

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pipenv install --system --deploy

# Expone el puerto por defecto de Flask
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=app.py

# Comando para ejecutar la app
CMD ["flask", "run", "--host=0.0.0.0"]
