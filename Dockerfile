FROM python:3.6
LABEL maintainer="ajhenaor"

COPY ./requirements.txt .
COPY ./docker-entrypoint-initdb.d .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
