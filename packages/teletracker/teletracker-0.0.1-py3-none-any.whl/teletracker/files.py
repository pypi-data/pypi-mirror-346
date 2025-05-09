#  Copyright (c) ChernV (@otter18), 2021.

import logging
import os # Import os module
from time import time, sleep
from typing import List

import telebot

# logging setup
logger = logging.getLogger(__name__)

# Supported image extensions
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']
FILE_EMOJI = "📎" # Emoji per i file


class TgFileLogger:
    """tg_logger tool to send files"""

    def __init__(self, token: str, users: List[int], timeout: int = 10):
        """
        Setup TgFileLogger tool

        :param token: tg bot token to log form
        :param users: list of used_id to log to
        :param timeout: seconds for retrying to send log if error occupied
        """

        self.token = token
        self.users = users
        self.timeout = timeout

        self.bot = telebot.TeleBot(token=self.token)

    def send(self, file_path: str, caption: str = ''):
        """
        Function to send file. Sends as photo if it's a recognized image type,
        otherwise sends as document.

        :param file_path: file path to log
        :param caption: text to file with file

        :return: None
        """
        if not os.path.exists(file_path):
            logger.error("File not found: %s", file_path)
            return

        _, file_extension = os.path.splitext(file_path)
        is_image = file_extension.lower() in IMAGE_EXTENSIONS

        # Prepend emoji to the caption
        final_caption = f"{FILE_EMOJI} {caption}" if caption else FILE_EMOJI

        try:
            with open(file_path, 'rb') as data:
                for user_id in self.users:
                    t0 = time()
                    while time() - t0 < self.timeout:
                        try:
                            # Reset file pointer for each user/retry
                            data.seek(0)
                            if is_image:
                                # Usa final_caption
                                self.bot.send_photo(user_id, photo=data, caption=final_caption, parse_mode="HTML")
                                logger.info("Image %s successfully sent to %s", file_path, user_id)
                            else:
                                # Usa final_caption
                                self.bot.send_document(user_id, document=data, caption=final_caption, parse_mode="HTML")
                                logger.info("File %s successfully sent to %s", file_path, user_id)
                            break # Exit retry loop on success
                        except telebot.apihelper.ApiException as e:
                            # Handle specific API errors if needed, e.g., file too large
                            logger.exception("Telegram API Exception while sending %s to %s: %s", file_path, user_id, e)
                            # Decide if retrying makes sense based on the error
                            if "file is too big" in str(e).lower(): # Example: Don't retry if file is too large
                                logger.error("File %s is too large to send.", file_path)
                                break # Stop trying for this user
                            sleep(1) # Wait before retrying for other errors
                        except Exception as e:
                            logger.exception("General Exception while sending %s to %s: %s", file_path, user_id, e)
                            sleep(1) # Wait before retrying
                    else:
                         logger.error("Timeout reached while trying to send %s to %s", file_path, user_id)

        except IOError as e:
            logger.error("Failed to open file %s: %s", file_path, e)
        except Exception as e:
            logger.error("An unexpected error occurred in send method for file %s: %s", file_path, e)
