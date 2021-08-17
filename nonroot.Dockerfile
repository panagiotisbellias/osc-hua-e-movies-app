# Use an existing docker image as a base
FROM python:3.9-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN groupadd appuser &&  useradd -g appuser -d  /app -M appuser

# change permission on workdir
RUN chown -R appuser:appuser /app

USER appuser:appuser
ENV PATH=$PATH:/app/.local/bin
#Change working directory

# COPY requirements.txt
COPY ./requirements.txt ./

RUN pip install -r requirements.txt
# Copy main.py file
COPY ./movies_app ./

USER root
RUN chown -R appuser:appuser /app

USER appuser:appuser

RUN python manage.py collectstatic --noinput
EXPOSE 8000/tcp

# Tell what to do when it starts as a container
CMD ["gunicorn" , "movies_app.wsgi:application", "--bind", " 0.0.0.0:8000"]