import gcsfs


def initialize_gcsfs():
    return gcsfs.GCSFileSystem()


def open_file(file_path: str, file_system: gcsfs.GCSFileSystem, mode: str = "rb"):
    return file_system.open(file_path, mode=mode)
