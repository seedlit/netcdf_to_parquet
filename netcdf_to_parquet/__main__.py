import argparse
import datetime
import logging
import pathlib
from typing import Optional

import gcsfs
import tqdm

from netcdf_to_parquet import constants, process_data, utils

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

file_system = utils.initialize_gcsfs()


def netcdf_to_parquet(
    file_path: str, output_path: str, file_system: gcsfs.GCSFileSystem
) -> None:
    """
    Convert a NetCDF file to a Parquet file.

    Args:
        file_path (str): The path to the NetCDF file in GCS.
        output_path (str): The output path for the Parquet file.
        file_system (gcsfs.GCSFileSystem): The GCS file system instance.

    Returns:
        None
    """
    try:
        dataframe = process_data.netcdf_to_dataframe(file_path, file_system)
        dataframe = process_data.add_h3_index(dataframe)
        process_data.save_dataframe_as_parquet(dataframe, output_path)
    except Exception as e:
        logging.error(f"Failed to process file {file_path}: {e}")
        raise


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process netCDF files and save as Parquet."
    )
    parser.add_argument(
        "start_date",
        type=lambda d: datetime.datetime.strptime(d, "%d-%m-%Y").date(),
        help="Start date in DD-MM-YYYY format",
    )
    parser.add_argument(
        "end_date",
        type=lambda d: datetime.datetime.strptime(d, "%d-%m-%Y").date(),
        help="End date in DD-MM-YYYY format",
    )
    parser.add_argument(
        "out_dir", type=str, help="Output directory for Parquet files"
    )
    return parser.parse_args()


def main(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    out_dir: str = "parquet_files",
    args: Optional[argparse.Namespace] = None,
) -> None:
    """
    Main function to process netCDF files and save as Parquet.

    Args:
        start_date (datetime.date, optional): Start date for processing. Defaults to None.
        end_date (datetime.date, optional): End date for processing. Defaults to None.
        out_dir (str): Output directory for Parquet files. Defaults to "parquet_files".
        args (argparse.Namespace, optional): Command-line arguments. Defaults to None.
    """
    if args is None and (
        start_date is None or end_date is None or out_dir is None
    ):
        args = parse_arguments()

    if start_date is None:
        start_date = args.start_date
    if end_date is None:
        end_date = args.end_date

    if start_date is None or end_date is None:
        raise ValueError("start_date and end_date must be provided.")

    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    current_date = start_date
    total_days = (end_date - current_date).days + 1
    for _ in tqdm.tqdm(range(total_days), desc="Processing dates"):
        try:
            date_str = current_date.strftime("%Y/%m/%d")
            file_path = f"{constants.GCS_BASE_URL}/{date_str}/total_precipitation/surface.nc"
            output_path = f"{out_dir}/precipitation_{current_date.strftime('%d_%m_%Y')}.parquet"
            netcdf_to_parquet(file_path, output_path, file_system)
        except Exception as e:
            logging.error(f"Failed to process date {current_date}: {e}")
        current_date += datetime.timedelta(days=1)


if __name__ == "__main__":
    main()
