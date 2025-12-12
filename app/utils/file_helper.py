import os
import lzma
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from io import BytesIO


class FileProcessor:
    CHUNK_SIZE = 64 * 1024  # 64KB per chunk

    def __init__(self, key: bytes):
        self.aes = AESGCM(key)

    # ------------------------
    # Encrypt + compress in memory → bytes
    # ------------------------
    def encrypt_and_compress_stream_bytes(self, input_file: str, output=None) -> bytes:
        with open(input_file, "rb") as f:
            data = f.read()
        compressed = lzma.compress(data, preset=9 | lzma.PRESET_EXTREME)
        nonce = os.urandom(12)
        encrypted = self.aes.encrypt(nonce, compressed, None)
        final = nonce + encrypted

        if output is None:
            return final
        elif isinstance(output, (str, os.PathLike)):
            with open(output, "wb") as out_file:
                out_file.write(final)
        else:
            output.write(final)


    # ------------------------
    # Decrypt + decompress in memory → write to file
    # ------------------------
    def decrypt_and_decompress_stream_bytes(self, input_stream, output=None) -> bytes | None:
        if isinstance(input_stream, (bytes, bytearray)):
            input_stream = BytesIO(input_stream)

        nonce = input_stream.read(12)
        encrypted_data = input_stream.read()
        decompressed = lzma.decompress(self.aes.decrypt(nonce, encrypted_data, None))

        if output is None:
            return decompressed
        elif isinstance(output, (str, os.PathLike)):
            with open(output, "wb") as out_file:
                out_file.write(decompressed)
        else:
            output.write(decompressed)
