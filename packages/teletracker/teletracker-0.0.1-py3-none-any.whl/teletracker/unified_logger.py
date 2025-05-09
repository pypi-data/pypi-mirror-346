import logging
from typing import List
from time import sleep

import requests # Assicurati che requests sia installato
import random
import io  # Aggiunto import
import traceback  # Aggiunto import
import html  # Add this import
from .files import TgFileLogger # Importa TgFileLogger

# Definisci qui gli emoji se non sono definiti altrove globalmente
INFO_EMOJIS = ["ℹ️", "💡", "➡️", "✅", "➡️"] # Esempio, adatta secondo necessità
DEFAULT_EMOJIS = {
    logging.DEBUG: "🐛",
    logging.INFO: "ℹ️",
    logging.WARNING: "⚠️",
    logging.ERROR: "❌",
    logging.CRITICAL: "🔥",
}

class UnifiedTgLogger(logging.Handler): # Eredita da logging.Handler
    """
    Provides a unified interface for logging messages and sending files
    via Telegram. Can be used as a handler for standard Python loggers.
    """

    def __init__(self, token: str, users: List[int], timeout: int = 10, level=logging.INFO, log_emoji: str | None = None, use_random_log_emoji: bool = False, disable_notification: bool = False, disable_web_page_preview: bool = False):
        """
        Initializes the UnifiedTgLogger.

        :param token: Telegram bot token.
        :param users: List of user IDs to send logs and files to.
        :param timeout: Timeout in seconds for sending messages/files.
        :param level: Logging level for the handler.
        :param log_emoji: Specific emoji to use for all log levels. Overrides use_random_log_emoji and default level emojis.
        :param use_random_log_emoji: If True and log_emoji is None, selects a random emoji from INFO_EMOJIS for all logs.
        :param disable_notification: Send the message silently. Users will receive a notification with no sound.
        :param disable_web_page_preview: Disables link previews for links in this message.
        """
        super().__init__(level=level) # Chiama il costruttore della classe base
        self.token = token
        self.users = users
        self.timeout = timeout
        self.log_emoji = log_emoji
        self.use_random_log_emoji = use_random_log_emoji
        self.disable_notification = disable_notification
        self.disable_web_page_preview = disable_web_page_preview
        
        # TgFileLogger rimane un componente separato per l'invio di file
        self.file_logger = TgFileLogger(token=self.token, users=self.users, timeout=self.timeout)

        # Non c'è più un logger interno, questa classe è l'handler.
        # Le chiamate a self.debug, self.info, ecc. non sono più necessarie
        # in quanto si userà il logger a cui questo handler è attaccato.

    def get_emoji(self, levelno: int) -> str:
        """Determines the emoji to use based on log level and configuration."""
        if self.log_emoji:
            return self.log_emoji
        if self.use_random_log_emoji:
            return random.choice(INFO_EMOJIS) if INFO_EMOJIS else ""
        return DEFAULT_EMOJIS.get(levelno, "")

    def emit(self, record: logging.LogRecord):
        """
        Formats and sends the log record to Telegram using HTML.
        The actual message content (record.msg) is formatted as HTML <code>,
        and the surrounding formatted parts are bolded using <b>.
        If exc_info is present, the traceback is appended as a <pre><code> block.
        """
        emoji = self.get_emoji(record.levelno)
        
        actual_message_content = record.getMessage()
        # Escape user-generated content for HTML
        escaped_actual_message_content = html.escape(actual_message_content)

        # Prepare for formatting with a placeholder
        placeholder = "___TG_LOGGER_MESSAGE_PLACEHOLDER___"
        original_msg = record.msg
        original_args = record.args
        
        original_message_attr_val = None
        had_message_attr = hasattr(record, 'message')
        if had_message_attr:
            original_message_attr_val = record.message
            delattr(record, 'message') # Force re-evaluation by formatter

        record.msg = placeholder
        record.args = () # Args were for original_msg, already incorporated into actual_message_content
        
        full_formatted_string_with_placeholder = self.format(record)
        
        # Restore the record to its original state
        record.msg = original_msg
        record.args = original_args
        if had_message_attr:
            record.message = original_message_attr_val
        elif hasattr(record, 'message'):
            delattr(record, 'message')

        # Construct the final message with HTML styling
        parts = full_formatted_string_with_placeholder.split(placeholder, 1)
        
        text_segments = []
        if emoji: # Ensure emoji is not empty before adding
             text_segments.append(emoji)

        prefix_html = ""
        # Core message is the actual log message, HTML escaped and in <code> tags
        core_message_html = f"<code>{escaped_actual_message_content}</code>"
        suffix_html = ""

        if len(parts) == 1: # Placeholder not found in format string (e.g., format was just %(asctime)s)
            # The entire formatted string is context, treat as prefix
            formatted_context_raw = parts[0].strip()
            if formatted_context_raw:
                prefix_html = f"<b>{html.escape(formatted_context_raw)}</b>"
        else: # Placeholder was found, len(parts) == 2
            prefix_raw = parts[0].strip()
            suffix_raw = parts[1].strip()

            if prefix_raw:
                prefix_html = f"<b>{html.escape(prefix_raw)}</b>"
            # core_message_html is already defined
            if suffix_raw:
                suffix_html = f"<b>{html.escape(suffix_raw)}</b>"
        
        # Assemble main message body parts
        # Emoji is already in text_segments if it exists
        
        if prefix_html:
            text_segments.append(prefix_html)
            # Add a newline before the core message if there was a prefix, similar to original Markdown version
            text_segments.append(f"\n{core_message_html}")
        else:
            text_segments.append(core_message_html)

        # if suffix_html:
        #     text_segments.append(suffix_html)
            
        message_to_send = " ".join(s for s in text_segments if s) # Join all non-empty parts with a space

        # Add traceback if present
        if record.exc_info:
            ei = record.exc_info
            sio = io.StringIO()
            # Replicates the core logic of logging.Handler.formatException
            traceback.print_exception(ei[0], ei[1], ei[2], limit=None, file=sio)
            s = sio.getvalue()
            sio.close()
            if s.endswith("\n"):
                s = s[:-1]
            traceback_str = s
            escaped_traceback_str = html.escape(traceback_str)
            # Ensure a newline before the traceback block
            message_to_send += f"\n<pre><code class=\"language-python\">{escaped_traceback_str}</code></pre>"
        
        for user_id in self.users:
            payload = {
                'chat_id': user_id,
                'text': message_to_send,
                'parse_mode': 'HTML', # Changed to HTML
                'disable_web_page_preview': self.disable_web_page_preview,
                'disable_notification': self.disable_notification,
            }
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            try:
                response = requests.post(url, data=payload, timeout=self.timeout)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                # Gestisci l'errore, ad esempio stampandolo o loggandolo altrove
                print(f"Error sending log to Telegram user {user_id}: {e}")
                self.handleError(record) # Metodo standard di logging.Handler

    def send_file(self, file_path: str, caption: str = ''):
        """
        Sends a file (document or photo) to the specified users.

        :param file_path: Path to the file to send.
        :param caption: Optional caption for the file.
        """
        self.file_logger.send(file_path=file_path, caption=caption)

    # Optional: Method to change log level dynamically
    def setLevel(self, level):
        """Sets the logging level."""
        super().setLevel(level) # Imposta il livello sull'handler stesso
        # Non è più necessario self.logger.setLevel(level)

    # Il metodo set_formatter è ereditato da logging.Handler,
    # ma se vuoi esporlo esplicitamente o modificarne il comportamento, puoi farlo.
    # Per ora, ci si aspetta che il formatter sia impostato sull'handler
    # quando viene aggiunto a un logger. Esempio:
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # tg_handler.setFormatter(formatter)

    # Optional: Method to add/remove users dynamically
    def update_users(self, users: List[int]):
        """Updates the list of users for both handler and file logger."""
        self.users = users
        self.file_logger.users = users

# Example usage (can be removed or kept for demonstration)
if __name__ == '__main__':
    # Replace with your actual token and user IDs
    BOT_TOKEN = "YOUR_BOT_TOKEN"
    USER_IDS = [123456789] # Example user ID

    if BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("Please replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot Token.")
    else:
        # --- Configura un logger standard ---
        logger = logging.getLogger('my_app_logger')
        logger.setLevel(logging.DEBUG) # Imposta il livello del logger principale

        # --- Esempio 1: UnifiedTgLogger come handler con emoji di default ---
        print("--- Initializing UnifiedTgLogger as handler (default emojis) ---")
        tg_handler_default = UnifiedTgLogger(token=BOT_TOKEN, users=USER_IDS, level=logging.INFO)
        # Imposta un formatter per l'handler
        formatter_default = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        tg_handler_default.setFormatter(formatter_default)
        logger.addHandler(tg_handler_default)

        logger.info("Default Handler: Info message from standard logger.")
        logger.warning("Default Handler: Warning message from standard logger.")
        logger.debug("Default Handler: Debug message (non dovrebbe apparire su Telegram se il livello dell'handler è INFO).")
        print("-----------------------------------------------------")
        sleep(2) # Pause between examples
        logger.removeHandler(tg_handler_default) # Rimuovi l'handler per non duplicare i messaggi

        # --- Esempio 2: UnifiedTgLogger con emoji specifico ---
        print("--- Initializing UnifiedTgLogger with a specific emoji (🔔) ---")
        tg_handler_specific = UnifiedTgLogger(token=BOT_TOKEN, users=USER_IDS, level=logging.INFO, log_emoji="🔔")
        formatter_specific = logging.Formatter('%(levelname)s: %(message)s') # Formatter diverso
        tg_handler_specific.setFormatter(formatter_specific)
        logger.addHandler(tg_handler_specific)

        logger.info("Specific Emoji Handler: Info message.")
        logger.error("Specific Emoji Handler: Error message.")
        print("-----------------------------------------------------")
        sleep(2)
        logger.removeHandler(tg_handler_specific)

        # --- Esempio 3: UnifiedTgLogger con emoji casuale ---
        print("--- Initializing UnifiedTgLogger with a random emoji ---")
        # Assicurati che INFO_EMOJIS sia definito se usi use_random_log_emoji=True
        # Per questo esempio, lo definiamo qui vicino se non è globale
        if 'INFO_EMOJIS' not in globals(): INFO_EMOJIS = ["🚀", "🌟", "🎉", "💡"]
        
        tg_handler_random = UnifiedTgLogger(token=BOT_TOKEN, users=USER_IDS, level=logging.WARNING, use_random_log_emoji=True)
        formatter_random = logging.Formatter('%(message)s') # Solo il messaggio
        tg_handler_random.setFormatter(formatter_random)
        logger.addHandler(tg_handler_random)

        logger.warning("Random Emoji Handler: A warning message.")
        logger.info("Random Emoji Handler: An info message (non dovrebbe apparire su Telegram se il livello dell'handler è WARNING).")
        logger.critical("Random Emoji Handler: A critical message!")
        print("-----------------------------------------------------")
        sleep(2)
        logger.removeHandler(tg_handler_random)

        # --- File Sending Example (usa il file_logger interno all'handler) ---
        print("--- Testing file sending (using one of the handlers) --- ")
        # Puoi usare qualsiasi istanza di UnifiedTgLogger per send_file
        # dato che TgFileLogger è inizializzato internamente.
        # Per chiarezza, ne creiamo una nuova o usiamo una esistente.
        file_sender_handler = UnifiedTgLogger(token=BOT_TOKEN, users=USER_IDS)

        dummy_file_path = "test_unified_handler.txt"
        with open(dummy_file_path, "w") as f:
            f.write("This is a test file sent via UnifiedTgLogger (as a handler).")

        print(f"Attempting to send file: {dummy_file_path}")
        file_sender_handler.send_file(dummy_file_path, caption="Test file via handler's send_file.")
        print("File send attempt finished.")

        # Clean up the dummy file
        import os
        try:
            os.remove(dummy_file_path)
            print(f"Removed dummy file: {dummy_file_path}")
        except OSError as e:
            print(f"Error removing dummy file {dummy_file_path}: {e}")

        print("Unified logger (as handler) example finished.")