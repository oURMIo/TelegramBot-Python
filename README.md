# Sagiri - Personal Telegram Assistant Bot

Sagiri is a personal Telegram assistant bot designed to help with server administration and everyday life tasks

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Installation

1. Clone the repository:

```shell
git clone https://github.com/oURMIo/telegram-bot.git
cd telegram-bot
```

2. Edit `pythonBot/config/config-example.ini`. More detailed instructions in the file

3. Build and start the Docker containers:

```shell
docker-compose up --build
```

4. Your bot should now be running. You can interact with it on Telegram.

## Usage

Once the bot is up and running, you can interact with it through Telegram. Add the bot to your contacts using its username and start a conversation.

## Built With

- Python 3.11
- python-telegram-bot
- Docker
- Docker Compose

## Authors

- oURMIo

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
