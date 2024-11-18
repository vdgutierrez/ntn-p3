# Usa una imagen base ligera de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Expone el puerto en el que correrá Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "run.py"]
