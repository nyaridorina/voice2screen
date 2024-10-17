FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that the application runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
