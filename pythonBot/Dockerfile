FROM python:3.11-slim-buster

WORKDIR ./pythonBot

RUN pip install --no-cache-dir -r pyTelegramBotAPI
RUN pip install --no-cache-dir -r TIME-python
RUN pip install --no-cache-dir -r requests-html

COPY ./pythonBot .

CMD [ "python", "main.py" ]
