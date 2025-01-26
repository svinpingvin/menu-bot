# Menu-Bot

Menu-Bot is a Telegram bot designed to help users generate meal plans and manage recipes. The bot supports adding dishes, organizing them into categories (breakfast, lunch, and dinner), and generating a menu for a specified period.

## Features

- **Dish Categories:** Add dishes under breakfast, lunch, or dinner categories.
- **Weighted Selection:** Each dish has a weight, increasing its probability of being chosen.
- **Menu Generation:** Generate a menu for a specified period (e.g., 2 weeks), ensuring variety and accommodating missing dishes with placeholders.
- **Multi-User Support:** Each user can have their own set of dishes, tied to their Telegram ID.

## Requirements

- Python 3.11
- PostgreSQL
- Poetry

## Setup

### Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Ensure Python 3.11 is installed on your local machine.
3. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/menu-bot.git
   cd menu-bot
   ```

### Configuration

1. Create a `.env` file in the root directory:
   ```env
   POSTGRES_USER=your_postgres_user
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

2. Update `pyproject.toml` with any additional dependencies.

### Building and Running the Bot

#### Using Docker Compose

   ```bash
   docker-compose up --build -d
   ```

#### Without Docker

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Set up the database:
   ```bash
   poetry run alembic upgrade head
   ```

3. Run the bot:
   ```bash
   poetry run python main.py
   ```