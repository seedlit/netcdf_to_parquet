import logging

import gcsfs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def initialize_gcsfs():
    logging.info("Initializing GCS file system")
    return gcsfs.GCSFileSystem(token="anon")


def open_file(
    file_path: str, file_system: gcsfs.GCSFileSystem, mode: str = "rb"
):
    return file_system.open(file_path, mode=mode)
