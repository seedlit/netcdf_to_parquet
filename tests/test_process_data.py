import pathlib
import tempfile

import pandas as pd
import pytest

from data_transformations import process_data

H3_INDEX = "890326233abffff"


@pytest.fixture
def test_dataframe():
    """
    Fixture to provide a test DataFrame.

    Returns:
        pd.DataFrame: The test DataFrame.
    """
    return pd.DataFrame(
        {
            "tp": [0.0],
            "longitude": [0.0],
            "latitude": [90.0],
            "time": ["22-01-01 00:00:00"],
        }
    )


def test_netcdf_to_dataframe(test_file_path, file_system):
    """
    Test the netcdf_to_dataframe function.

    Args:
        test_file_path (str): The path to the test NetCDF file.
    """
    df = process_data.netcdf_to_dataframe(test_file_path, file_system)
    assert set(df.columns) == {"tp", "longitude", "time", "latitude"}
    assert len(df) == 24917760


def test_add_h3_index(test_dataframe):
    """
    Test the add_h3_index function.

    Args:
        test_dataframe (pd.DataFrame): The test DataFrame.
    """
    df_with_h3 = process_data.add_h3_index(test_dataframe)
    assert set(df_with_h3.columns) == {
        "tp",
        "longitude",
        "latitude",
        "time",
        "h3_index",
    }
    assert len(df_with_h3) == 1
    assert df_with_h3["h3_index"].values == H3_INDEX


def test_save_dataframe_as_parquet(test_dataframe):
    """
    Test the save_dataframe_as_parquet function.

    Args:
        test_dataframe (pd.DataFrame): The test DataFrame.
    """
    test_dataframe["h3_index"] = [H3_INDEX]
    with tempfile.NamedTemporaryFile(suffix=".parquet") as temp_file:
        output_path = temp_file.name
        process_data.save_dataframe_as_parquet(test_dataframe, output_path)
        assert pathlib.Path(output_path).exists()
