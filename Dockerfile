FROM python:3.7-slim

WORKDIR /columnpubbot

COPY requirements.txt /columnpubbot/
RUN pip install -r /columnpubbot/requirements.txt
COPY . /columnpubbot/

CMD python3 /columnpubbot/app.py