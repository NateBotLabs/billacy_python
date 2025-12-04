"""Logger configuration for the Invoice Application.
"""
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("InvoiceApp")
logger.setLevel(logging.DEBUG)  # Log everything DEBUG and above

# Console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Print debug to console
console_format = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(console_format)

# File handler for errors/warnings/info
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.INFO)  # Only log INFO and above to file
file_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_format)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
