import pathlib
import tempfile

import pandas as pd
import pytest

from src import constants, process_data, utils

#  TODO: add a note that all of these are live tests


@pytest.fixture
def test_file_path():
    return f"{constants.GCS_BASE_URL}/2022/01/01/total_precipitation/surface.nc"


@pytest.fixture
def test_dataframe():
    return pd.DataFrame(
        {
            "tp": [0.0],
            "longitude": [0.0],
            "latitude": [90.0],
            "time": ["22-01-01 00:00:00"],
        }
    )


def test_netcdf_to_dataframe(test_file_path):
    file_system = utils.initialize_gcsfs()
    df = process_data.netcdf_to_dataframe(test_file_path, file_system)
    assert set(df.columns) == {"tp", "longitude", "time", "latitude"}
    assert len(df) == 24917760


def test_add_h3_index(test_dataframe):
    df_with_h3 = process_data.add_h3_index(test_dataframe)
    assert set(df_with_h3.columns) == {
        "tp",
        "longitude",
        "latitude",
        "time",
        "h3_index",
    }
    assert len(df_with_h3) == 1
    assert df_with_h3["h3_index"].values == "890326233abffff"


def test_save_dataframe_as_parquet(test_dataframe):
    test_dataframe["h3_index"] = ["890326233abffff"]
    with tempfile.NamedTemporaryFile(suffix=".parquet") as temp_file:
        output_path = temp_file.name
        process_data.save_dataframe_as_parquet(test_dataframe, output_path)
        assert pathlib.Path(output_path).exists()
