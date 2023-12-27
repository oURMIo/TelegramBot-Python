FROM python:3.11-slim-buster

WORKDIR ./pythonBot

RUN pip install --no-cache-dir pyTelegramBotAPI
RUN pip install --no-cache-dir TIME-python
RUN pip install --no-cache-dir requests-html

COPY . .

CMD [ "python", "src/main.py" ]
