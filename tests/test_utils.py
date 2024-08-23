import gcsfs

from src import utils


def test_initialize_gcsfs():
    assert isinstance(utils.initialize_gcsfs(), gcsfs.GCSFileSystem)


def test_open_file():
    file_system = utils.initialize_gcsfs()
    file_path = "gs://gcp-public-data-arco-era5/raw/date-variable-single_level/2022/01/01/total_precipitation/surface.nc"
    with utils.open_file(file_path, file_system) as f:
        assert f.readable()
        assert f.seekable()
        assert f.mode == "rb"
