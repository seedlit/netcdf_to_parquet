import gcsfs
import pytest

from transform import constants, utils


@pytest.fixture
def test_file_path():
    """
    Fixture to provide a test file path for NetCDF files in GCS.

    Returns:
        str: The path to the test NetCDF file in GCS.
    """
    return (
        f"{constants.GCS_BASE_URL}/2022/01/01/"
        "total_precipitation/surface.nc"
    )


@pytest.fixture
def file_system() -> gcsfs.GCSFileSystem:
    """
    Fixture to provide a GCS file system instance.

    Returns:
        gcsfs.GCSFileSystem: The GCS file system instance.
    """
    return utils.initialize_gcsfs()
