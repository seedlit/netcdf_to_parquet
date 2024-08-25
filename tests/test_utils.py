import gcsfs

from netcdf_to_parquet import utils


def test_initialize_gcsfs():
    """
    Test the initialize_gcsfs function.
    """
    assert isinstance(utils.initialize_gcsfs(), gcsfs.GCSFileSystem)


def test_open_file(test_file_path, file_system):
    """
    Test the open_file function.

    Args:
        test_file_path (str): The path to the test file.
        file_system (gcsfs.GCSFileSystem): The GCS file system instance.
    """
    with utils.open_file(test_file_path, file_system) as f:
        assert f.readable()
        assert f.seekable()
        assert f.mode == "rb"
