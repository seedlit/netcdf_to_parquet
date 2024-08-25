import logging

import gcsfs
import h3
import pandas as pd
import xarray as xr

from . import utils

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def netcdf_to_dataframe(
    file_path: str, file_system: gcsfs.GCSFileSystem
) -> pd.DataFrame:
    """
    Convert a NetCDF file to a Pandas DataFrame.

    Args:
        file_path (str): The path to the NetCDF file in GCS.
        file_system (gcsfs.GCSFileSystem): The GCS file system instance.

    Returns:
        pd.DataFrame: The converted DataFrame.
    """
    logging.info("Streaming data from GCS bucket for %s", file_path)
    try:
        with utils.open_file(file_path, file_system, mode="rb") as f:
            return xr.open_dataset(f).to_dataframe().reset_index()
    except Exception as e:
        logging.error(f"Failed to convert NetCDF to DataFrame: {e}")
        raise


def add_h3_index(dataframe: pd.DataFrame, resolution: int = 9) -> pd.DataFrame:
    """
    Add H3 index to the DataFrame based on latitude and longitude.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        resolution (int, optional): The H3 resolution. Defaults to 9.

    Returns:
        pd.DataFrame: The DataFrame with H3 index added.
    """
    try:
        dataframe["h3_index"] = dataframe.apply(
            lambda row: h3.geo_to_h3(
                row["latitude"], row["longitude"], resolution=resolution
            ),
            axis=1,
        )
        return dataframe
    except Exception as e:
        logging.error(f"Failed to add H3 index: {e}")
        raise


def save_dataframe_as_parquet(dataframe: pd.DataFrame, out_path: str) -> None:
    """
    Save the DataFrame as a Parquet file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        out_path (str): The output path for the Parquet file.

    Returns:
        None
    """
    logging.info("Saving DataFrame to Parquet file at %s", out_path)
    try:
        dataframe.to_parquet(out_path, engine="pyarrow")
    except Exception as e:
        logging.error(f"Failed to save DataFrame as Parquet: {e}")
        raise
