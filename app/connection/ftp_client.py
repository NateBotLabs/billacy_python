import os
import time
from io import BytesIO
from ftplib import FTP, error_perm, all_errors
from pathlib import Path
from dotenv import load_dotenv
from functools import wraps
from typing import Optional
from app.utils.errors import UnknownEnvironmentError, FTPConnectionError


def require_connection(func):
    """
    Decorator to ensure FTP connection is initialized before method execution.
    """
    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        if cls._ftp is None:
            raise FTPConnectionError("FTP not connected")
        return func(cls, *args, **kwargs)
    return wrapper


class FTPClient:
    """
    FTP client with environment-based configuration, automatic retries, 
    passive mode support, and safe upload/download utilities.
    """

    _ftp: Optional[FTP] = None
    _env: Optional[str] = None
    CACHE_DIR: Path = Path(".cache/media")
    RETRY_COUNT: int = 3  # Number of retries for transient errors
    RETRY_DELAY: float = 2.0  # Seconds to wait between retries

    @classmethod
    def initialize(cls, env: Optional[str] = None, passive: bool = True, timeout: int = 10) -> FTP:
        """
        Initialize FTP connection. If already connected, returns existing connection.
        Supports passive mode and configurable timeout.

        Args:
            env (Optional[str]): Environment ('development' or 'test'). Defaults to system ENV or 'development'.
            passive (bool): Whether to use passive FTP mode. Defaults to True.
            timeout (int): Connection timeout in seconds. Defaults to 10.

        Returns:
            FTP: Active FTP connection.

        Raises:
            UnknownEnvironmentError: Invalid environment.
            FTPConnectionError: Connection or login failure.
            RuntimeError: Missing environment variables.
        """
        if cls._ftp is not None:
            return cls._ftp

        cls._env = env or os.getenv("ENV", "development").lower()
        if cls._env not in ("development", "test"):
            raise UnknownEnvironmentError(f"Unknown environment: {cls._env}")

        # Load environment variables
        load_dotenv(f".env.{cls._env}.local")
        host = os.getenv("FTP_HOST")
        user = os.getenv("FTP_USER")
        passwd = os.getenv("FTP_PASS")
        port = int(os.getenv("FTP_PORT", "21"))

        if not all([host, user, passwd]):
            raise RuntimeError(
                f"Missing FTP environment variables in .env.{cls._env}.local")

        # Attempt connection with retries
        last_error = None
        for attempt in range(1, cls.RETRY_COUNT + 1):
            try:
                ftp = FTP()
                ftp.connect(host, port, timeout=timeout)
                ftp.login(user, passwd)
                ftp.set_pasv(passive)
                cls._ftp = ftp
                cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
                return cls._ftp
            except all_errors as e:
                last_error = e
                print(f"[FTP] Attempt {attempt}/{cls.RETRY_COUNT} failed: {e}")
                time.sleep(cls.RETRY_DELAY)

        raise FTPConnectionError(
            f"Failed to connect to FTP server after {cls.RETRY_COUNT} attempts: {last_error}") from last_error

    @classmethod
    @require_connection
    def upload_bytes(cls, data: bytes, remote_path: str) -> None:
        """
        Upload raw bytes to FTP server with retries.

        Args:
            data (bytes): Data to upload.
            remote_path (str): Path on the server.
        """
        for attempt in range(1, cls.RETRY_COUNT + 1):
            try:
                with BytesIO(data) as bio:
                    cls._ftp.storbinary(f"STOR {remote_path}", bio)
                print(f"[FTP] Uploaded {len(data)} bytes → {remote_path}")
                return
            except all_errors as e:
                print(
                    f"[FTP] Upload attempt {attempt}/{cls.RETRY_COUNT} failed: {e}")
                time.sleep(cls.RETRY_DELAY)

        raise FTPConnectionError(
            f"Failed to upload {remote_path} after {cls.RETRY_COUNT} attempts.")

    @classmethod
    @require_connection
    def download_bytes(cls, remote_path: str) -> bytes:
        """
        Download file from FTP server as bytes with retries.

        Args:
            remote_path (str): Path of file on server.

        Returns:
            bytes: Downloaded data.
        """
        for attempt in range(1, cls.RETRY_COUNT + 1):
            try:
                data: list[bytes] = []
                cls._ftp.retrbinary(f"RETR {remote_path}", data.append)
                print(f"[FTP] Downloaded {remote_path}")
                return b"".join(data)
            except all_errors as e:
                print(
                    f"[FTP] Download attempt {attempt}/{cls.RETRY_COUNT} failed: {e}")
                time.sleep(cls.RETRY_DELAY)

        raise FTPConnectionError(
            f"Failed to download {remote_path} after {cls.RETRY_COUNT} attempts.")

    @classmethod
    @require_connection
    def list_files(cls, path: str = ".") -> list[str]:
        """
        List files in a directory on the FTP server.

        Args:
            path (str): Directory path on server.

        Returns:
            list[str]: List of files/directories.
        """
        try:
            return cls._ftp.nlst(path)
        except all_errors as e:
            raise FTPConnectionError(
                f"Failed to list files in {path}: {e}") from e

    @classmethod
    @require_connection
    def close(cls) -> None:
        """
        Gracefully close the FTP connection.
        """
        try:
            cls._ftp.quit()
        except error_perm:
            cls._ftp.close()
        finally:
            cls._ftp = None
            print("[FTP] Connection closed.")
