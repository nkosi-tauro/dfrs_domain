FROM python:3.10-alpine

# Create working directory
WORKDIR /app

# copy requirements.txt into directory
COPY requirements.txt requirements.txt
# Install packages from requirements.txt + Adde some config for postgres
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
# Copy local directory into /app
COPY . .

# Expose port 8000
EXPOSE 8000

CMD ["python3", "manage.py" , "runserver", "0.0.0.0:8000"]