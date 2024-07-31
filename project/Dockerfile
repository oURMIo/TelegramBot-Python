FROM python:3.11-slim-buster

WORKDIR ./project

RUN pip install --no-cache-dir pyTelegramBotAPI
RUN pip install --no-cache-dir TIME-python
RUN pip install --no-cache-dir requests-html
RUN pip install --no-cache-dir lxml_html_clean

COPY . .

CMD [ "python", "telegram_bot/main.py" ]
