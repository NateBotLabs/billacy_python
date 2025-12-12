import os
import base64
from pathlib import Path
from app.repositories.registry import RepoRegistry, RepoName
from app.models.media import Media
from app.utils.logger import logger
from app.utils.file_helper import FileProcessor
from app.connection.ftp_client import FTPClient


class SettingsService:
    PROFILE_FOLDER = "pictures"
    DOCUMENTS_FOLDER = "documents"
    OTHER_MEDIA_FOLDER = "other"
    CACHE_DIR = Path(".cache/media")

    def __init__(self):
        key = base64.b64decode(os.getenv("FILE_ENCRYPTION_KEY"))
        self.processor = FileProcessor(key)
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        logger.debug("Initializing SettingsService")

    # ------------------------
    # Upload methods
    # ------------------------
    def upload_profile_photo(self, local_path: str | Path):
        self._validate_local_path(local_path)
        original_filename = Path(local_path).name
        storage_filename = f"{original_filename}.{os.urandom(6).hex()}.enc"
        remote_path = f"{self.PROFILE_FOLDER}/{storage_filename}"

        logger.info("Uploading profile photo: %s → %s", original_filename, storage_filename)

        # Encrypt + compress locally then stream upload
        data = self.processor.encrypt_and_compress_stream_bytes(str(local_path))
        FTPClient.upload_bytes(data, remote_path)
        self._save_metadata("profile", original_filename, storage_filename)

    def upload_document(self, local_path: str | Path):
        self._validate_local_path(local_path)
        original_filename = Path(local_path).name
        storage_filename = f"{original_filename}.{os.urandom(6).hex()}.enc"
        remote_path = f"{self.DOCUMENTS_FOLDER}/{storage_filename}"

        logger.info("Uploading document: %s → %s", original_filename, storage_filename)
        data = self.processor.encrypt_and_compress_stream_bytes(str(local_path))
        FTPClient.upload_bytes(data, remote_path)
        self._save_metadata("document", original_filename, storage_filename)

    def upload_other_media(self, local_path: str | Path):
        self._validate_local_path(local_path)
        original_filename = Path(local_path).name
        storage_filename = f"{original_filename}.{os.urandom(6).hex()}.enc"
        remote_path = f"{self.OTHER_MEDIA_FOLDER}/{storage_filename}"

        logger.info("Uploading media: %s → %s", original_filename, storage_filename)
        data = self.processor.encrypt_and_compress_stream_bytes(str(local_path))
        FTPClient.upload_bytes(data, remote_path)
        self._save_metadata("media", original_filename, storage_filename)

    # ------------------------
    # Download / Streaming methods
    # ------------------------
    def download_profile_photo(self, target_path: str | Path):
        media = self.get_profile_photo()
        if not media:
            return None
        target_path = Path(target_path)
        remote_path = f"{self.PROFILE_FOLDER}/{media.storage_filename}"

        encrypted_bytes = FTPClient.download_bytes(remote_path)
        self.processor.decrypt_and_decompress_stream_bytes(encrypted_bytes, target_path)
        return target_path

    def download_document(self, media: Media, target_path: str | Path):
        remote_path = f"{self.DOCUMENTS_FOLDER}/{media.storage_filename}"
        encrypted_bytes = FTPClient.download_bytes(remote_path)
        self.processor.decrypt_and_decompress_stream_bytes(encrypted_bytes, target_path)
        return target_path

    def download_other_media(self, media: Media, target_path: str | Path):
        remote_path = f"{self.OTHER_MEDIA_FOLDER}/{media.storage_filename}"
        encrypted_bytes = FTPClient.download_bytes(remote_path)
        self.processor.decrypt_and_decompress_stream_bytes(encrypted_bytes, target_path)
        return target_path

    # ------------------------
    # Metadata retrieval
    # ------------------------
    def get_profile_photo(self) -> Media | None:
        return self.get_latest("profile")

    def get_documents(self) -> list[Media]:
        return self.get_all("document")

    def get_other_media(self) -> list[Media]:
        return self.get_all("media")

    def get_latest(self, category: str) -> Media | None:
        return RepoRegistry.get(RepoName.MEDIA).get_latest(
            Media.category == category,
            Media.uploaded_at
        )

    def get_all(self, category: str) -> list[Media]:
        return RepoRegistry.get(RepoName.MEDIA).get_all(
            Media.category == category
        )

    # ------------------------
    # Internal helpers
    # ------------------------
    def _save_metadata(self, category: str, original_filename: str, storage_filename: str):
        media = Media(category=category, original_filename=original_filename,
                      storage_filename=storage_filename)
        RepoRegistry.get(RepoName.MEDIA).insert(media)

    @staticmethod
    def _validate_local_path(local_path: str | Path):
        if not isinstance(local_path, (str, Path)):
            raise TypeError(f"Expected file path, got {type(local_path).__name__}")
        path = Path(local_path)
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
