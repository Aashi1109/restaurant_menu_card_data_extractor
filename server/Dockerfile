FROM python:3.12

LABEL authors="Ashish Pal"

LABEL version="1.0.0"

WORKDIR /server

COPY requirements.txt /server

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./src /server

CMD ["python", "-m", "src/main.py"]