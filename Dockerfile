### pip freeze -l > requirements.txt ### to create a new requirements.txt file

# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . .

EXPOSE 8000
EXPOSE 8001

CMD [ "python", "manage.py", "runserver"]