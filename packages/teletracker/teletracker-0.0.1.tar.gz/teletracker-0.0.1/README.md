# Teletracker

[![PyPI version](https://img.shields.io/pypi/v/teletracker.svg)](https://pypi.org/project/teletracker)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A bridge between Python's `logging` module and Telegram: send log messages and files directly to your chat.

## 📦 Installation

Install the package from PyPI with:

```bash
pip install teletracker
```

## 🚀 Overview

The library provides a handler for Python's logging framework and a dedicated class for sending files via Telegram.

### Main Classes

#### `UnifiedTgLogger`

Inherits from `logging.Handler`; sends formatted log messages via Telegram.

Constructor:

```python
UnifiedTgLogger(
    token: str,
    users: List[int],
    timeout: int = 10,
    level: int = logging.INFO,
    log_emoji: Optional[str] = None,
    use_random_log_emoji: bool = False,
    disable_notification: bool = False,
    disable_web_page_preview: bool = False
)
```

Parameters:

- `token` – Telegram bot token.
- `users` – List of `chat_id` to send logs to.
- `timeout` – HTTP timeout in seconds.
- `level` – Log level (default `INFO`).
- `log_emoji` – Fixed emoji for all messages.
- `use_random_log_emoji` – If `True`, chooses a random emoji.
- `disable_notification` – Send silently.
- `disable_web_page_preview` – Disable link previews.

Methods:

- `get_emoji(levelno: int) -> str`
  Returns the emoji based on the log level or settings.

- `emit(record: logging.LogRecord)`
  Formats the record with HTML and sends the message to the bot. If `exc_info` is present, includes the traceback in a `<pre><code>` block.

- `send_file(file_path: str, caption: str = '')`
  Sends a file (document or image); delegates to `TgFileLogger`.

- `setLevel(level: int)`
  Dynamically changes the log level of the handler.

- `update_users(users: List[int])`
  Updates the list of users (chat_id) for messages and files.

#### `TgFileLogger`

Dedicated class for sending files via Telegram. Can be used directly or through `UnifiedTgLogger`.

Constructor:

```python
TgFileLogger(
    token: str,
    users: List[int],
    timeout: int = 10
)
```

Main method:

- `send(file_path: str, caption: str = '')`
  Sends a document or image with an optional caption.

## 📖 Usage Examples

### Simple Logging

```python
import logging
from teletracker.unified_logger import UnifiedTgLogger

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

handler = UnifiedTgLogger(
    token='YOUR_BOT_TOKEN_HERE',  # Replace with your bot token
    users=[YOUR_CHAT_ID_HERE]     # Replace with your chat ID
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Application started')
logger.error('An error was recovered')

try:
    1/0
except Exception:
    logger.exception('Division by zero occurred')
```

### Sending Files

```python
from teletracker.unified_logger import UnifiedTgLogger

# Assuming 'token' and 'users' are defined as in the simple logging example
# token = 'YOUR_BOT_TOKEN_HERE'
# users = [YOUR_CHAT_ID_HERE]

file_logger = UnifiedTgLogger(token, users) # Or TgFileLogger(token, users)
file_logger.send_file(
    'report.txt',
    caption='Daily report'
)
```

## 🙏 Acknowledgements

This project was originally forked from [otter18/tg_logger](https://github.com/otter18/tg_logger).
The original library provided a great starting point. This fork was created because the original project was no longer actively maintained and lacked certain features.
While the codebase has been significantly refactored and rewritten to add new functionalities and improvements, we acknowledge the foundational work of the original author.

## 📜 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

