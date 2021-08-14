FROM python:3.9.buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install requirements.txt
COPY movies_app ./
EXPOSE 8000/tcp
CMD ["gunicorn" , ""]