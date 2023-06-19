FROM python:3.10-alpine

# Create working directory
WORKDIR /app

# copy requirements.txt into directory
COPY requirements.txt requirements.txt
# Install packages from requirements.txt
RUN pip3 install -r requirements.txt
# Copy local directory into /app
COPY . .

CMD ["python3", "manage.py" , "runserver", "0.0.0.0:8000"]