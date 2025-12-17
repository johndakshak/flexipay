# my python image
FROM python:3.9-slim

# cd into my working directory
WORKDIR /app

# copy requirement file into the present directory
COPY requirements.txt .

# installing dependencies i need and not storing cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# copies everything from host folder into the container's working directory
COPY . .

# listens to port 8000
EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]