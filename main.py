"""main entry point for the app"""
# main.py
import os
import sys
from app.connection.setup import DatabaseSetup
from app.connection.ftp_client import FTPClient
from app.gui.app import run_app
from app.utils.logger import logger
from app.utils.errors import UnexpectedError

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.stdout.reconfigure(encoding='utf-8')


def main():
    """Main entry point for the Billacy application."""
    os.environ.setdefault("ENV", "development")

    try:
        # Initialize database connection
        session = DatabaseSetup.initialize()
        if session is None:
            logger.error("Failed to connect to database. Exiting...")
            sys.exit(1)
        
        ftp = FTPClient.initialize()
        if ftp is None:
            logger.error("Failed to connect to FTP server. Exiting...")
            sys.exit(1)

        # Launch GUI
        run_app()

    except UnexpectedError as e:
        logger.exception("Unexpected error occurred: %s", e)
        sys.exit(1)

    finally:
        # Close DB session safely on exit
        DatabaseSetup.close()
        FTPClient.close()
        logger.info("Application shutdown, DB session closed.")


if __name__ == "__main__":
    main()
