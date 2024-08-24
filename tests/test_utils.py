import gcsfs

from src import utils


def test_initialize_gcsfs():
    assert isinstance(utils.initialize_gcsfs(), gcsfs.GCSFileSystem)


def test_open_file(test_file_path):
    file_system = utils.initialize_gcsfs()
    with utils.open_file(test_file_path, file_system) as f:
        assert f.readable()
        assert f.seekable()
        assert f.mode == "rb"
