import argparse
import datetime
import logging
import pathlib

import gcsfs
import tqdm

from src import constants, process_data, utils

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

file_system = utils.initialize_gcsfs()


def netcdf_to_parquet(
    file_path: str, output_path: str, file_system: gcsfs.GCSFileSystem
):
    dataframe = process_data.netcdf_to_dataframe(file_path, file_system)
    dataframe = process_data.add_h3_index(dataframe)
    process_data.save_dataframe_as_parquet(dataframe, output_path)


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

args = parser.parse_args()
pathlib.Path(args.out_dir).mkdir(parents=True, exist_ok=True)

current_date = args.start_date
total_days = (args.end_date - current_date).days + 1

for _ in tqdm.tqdm(range(total_days), desc="Processing dates"):
    try:
        date_str = current_date.strftime("%Y/%m/%d")
        file_path = (
           f"{constants.GCS_BASE_URL}/{date_str}/total_precipitation/surface.nc"
        )
        output_path = (
            f"{args.out_dir}/precipitation_{current_date.strftime('%d_%m_%Y')}.parquet"
        )
        netcdf_to_parquet(file_path, output_path, file_system)
    except Exception as e:
        logging.error(
            f"Failed to process date {current_date.strftime('%d_%m_%Y')}: {e}"
        )
    finally:
        current_date += datetime.timedelta(days=1)
