# Black Clover Quiz Bot

[Русская версия Readme (Описания)](README.ru.md)  

## Description

Quotes from characters of "Black Clover", where you need to guess which character said the quote.
Currently, 10 quotes are available.

## How to Play?

The bot runs on a remote server. [Try playing with it now!](https://t.me/blackclover_quiz_bot)

## Key Features

*   **Multilingual support:** Supports multiple languages (Russian and English) with the ability to switch "on the fly".
*   **Redis:** Uses Redis to store user data (language, number of completions), ensuring fast and efficient state management.
*   **Finite State Machine (FSM):** Implements FSM logic to manage the quiz process, providing a structured and predictable user experience.
*   **Randomization:** Character options for each quote are randomized, as well as the position of the correct character button (the one whose quote it is).
*   **Advanced logging:** Uses Loguru for detailed tracking of the bot’s operation and quick error detection.
*   **Clean architecture:** The project is divided into modules for easier development, testing, and scaling.

    *   `config/`: Application configuration.
    *   `handlers/`: Telegram event handlers.
    *   `keyboards/`: Bot keyboards.
    *   `lexicon/`: Text content
    *   `middlewares/`: Middleware for request processing.
    *   `states/`: FSM state definitions.
    *   `utils/`: Utility functions.
    *   `main.py`: Entry point
    *   `env.example`: Example of how to fill `.env`


## Technology Stack

*   Python 3.13
*   Aiogram 3.20
*   Redis
