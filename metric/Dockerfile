FROM python:3.12

WORKDIR /evgeniya/src/app

COPY ./src/ ./

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./metric.py" ]