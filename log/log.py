import logging 
import time
import os

from pathlib import Path

# Longer
logger = logging.getLogger(__name__)

# Handlers
file_handler = logging.FileHandler(f"{os.path.join(Path().absolute(), 'log', 'logs', 'app.log')}", mode="a")
file_handler.setLevel(logging.DEBUG)

# Formatters
logging.Formatter.converter = time.gmtime
formatter = logging.Formatter(
  '[%(asctime)s] - %(filename)s - line: %(lineno)d - function: %(funcName)s - %(levelname)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S'
)

file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
