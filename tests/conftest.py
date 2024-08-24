import pytest

from src import constants


@pytest.fixture
def test_file_path():
    return (
        f"{constants.GCS_BASE_URL}/2022/01/01/"
        "total_precipitation/surface.nc"
    )
