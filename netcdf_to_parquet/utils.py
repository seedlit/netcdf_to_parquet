import logging

import gcsfs

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def initialize_gcsfs():
    """
    Initialize the Google Cloud Storage file system.
    This function sets up the GCS file system using anonymous access.

    Returns:
        gcsfs.GCSFileSystem: An instance of the GCSFileSystem.
    """
    logging.info("Initializing GCS file system")
    try:
        return gcsfs.GCSFileSystem(token="anon")
    except Exception as e:
        logging.error(f"Failed to initialize GCS file system: {e}")
        raise


def open_file(
    file_path: str, file_system: gcsfs.GCSFileSystem, mode: str = "rb"
):
    """
    Open a file from the Google Cloud Storage file system.

    Args:
        file_path (str): The path to the file in GCS.
        file_system (gcsfs.GCSFileSystem): The GCS file system instance.
        mode (str, optional): The mode in which to open the file. Defaults to "rb".

    Returns:
        gcsfs.core.GCSFile: The opened file object.
    """
    logging.info(f"Opening file {file_path} in mode {mode}")
    try:
        return file_system.open(file_path, mode=mode)
    except Exception as e:
        logging.error(f"Failed to open file {file_path}: {e}")
        raise
