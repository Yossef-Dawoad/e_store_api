FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app


COPY requirements.txt .


RUN python3 -m pip install --upgrade pip

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application from the current directory to /app in the container
COPY . .

EXPOSE 8000

# run the uvicorn server
CMD [ "fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "--reload" ]