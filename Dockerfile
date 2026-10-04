# Use a lightweight official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the serialized model and Flask API code to the container
COPY superkart_sales_prediction_model.pkl .
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run the web application using Gunicorn for production suitability
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]