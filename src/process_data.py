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
    logging.info("Streaming data from GCS bucket for %s", file_path)
    with utils.open_file(file_path, file_system, mode="rb") as f:
        return xr.open_dataset(f).to_dataframe().reset_index()


def add_h3_index(dataframe: pd.DataFrame, resolution: int = 9) -> pd.DataFrame:
    dataframe["h3_index"] = dataframe.apply(
        lambda row: h3.geo_to_h3(
            row["latitude"], row["longitude"], resolution=resolution
        ),
        axis=1,
    )
    return dataframe


def save_dataframe_as_parquet(dataframe: pd.DataFrame, out_path: str) -> None:
    dataframe.to_parquet(out_path, engine="pyarrow")
