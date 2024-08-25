# Data Transformation pipeline: NetCDF to Parquet


This pipeline transforms total precipitation NetCDF files into Parquet format. <br/>
The source data is publicly available and is hosted at `gs://gcp-public-data-arco-era5/raw/date-variable-single_level`.

The transformed data supports:
 - regular queries with filtering with timestamp.
 - filtering by H3 geospatial index

## Installation

### Using Docker
To build the docker image, run:
```sh
docker build -t netcdf_to_parquet .
```

To run the docker container, here's an example command:
`docker run -v $(pwd)/output:/app/output netcdf_to_parquet <start_date> <end_date> <out_dir>`
<br/>
Here, `start_date` and `end_date` are in DD-MM-YYYY format. 
<br/>
And `out_dir` is the directory where the parquet files will be generated. 

For example:
```sh
docker run -v $(pwd)/output:/app/output netcdf_to_parquet 01-01-2022 04-01-2022 out_dir
```

### Using Poetry
Poetry makes life easier for managing dependencies and creating environments. Note that you need to have Poetry pre-installed in your system. To install Poetry, follow the steps listed [here](https://python-poetry.org/docs/#installation).

To generate and activate the environment, run following commands from the root directory:
```sh
poetry install
poetry shell
python -m netcdf_to_parquet 01-01-2023 03-01-2023 ./parquet_files
```

### Using pip
For the ease of usability, this is also available on [test pypi](https://test.pypi.org) (protype stage).
<br/>
To install it in your python environment, run:
```sh
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ netcdf-to-parquet 
```

To generate files in Apache parquet format, here's an example command:
```sh
import datetime
import netcdf_to_parquet

netcdf_to_parquet.main(
    start_date=datetime.date(2022, 1, 1),
    end_date=datetime.date(2022, 1, 4),
    out_dir="parquet_files",
)
```

## Queries
Once you have generated the parquet files, you can load it as a dataframe and run queries on timestamp, H3 index, etc.
<br/>
Here's an end to end example to generate a parquet file for total precipitation data from January 1, 2022 and then run queries on it.

```sh
import datetime
import pandas as pd
import netcdf_to_parquet

netcdf_to_parquet.main(
    start_date=datetime.date(2022, 1, 1),
    end_date=datetime.date(2022, 1, 1),
    out_dir="parquet_files",
)
dataframe = pd.read_parquet("parquet_files/precipitation_01_01_2022.parquet")

# filtering by datetime
filter_timestamp = pd.Timestamp("2022-01-01 02:00:00")
filtered_dataframe = dataframe[dataframe["time"] == filter_timestamp]
print(filtered_dataframe.head())

# filtering by H3 indexing
filtered_dataframe = dataframe[dataframe["h3_index"] == "890326233abffff"]
print(filtered_dataframe.head())
```

### Features


 - To avoid saving the source file locally, this project uses [gcsfs](https://github.com/fsspec/gcsfs) to stream the source NetCDF file into memory.

 - Pre-commit Hooks: This project uses pre-commit hooks to ensure code quality. To set up pre-commit hooks, run:

    ```sh
    poetry run pre-commit install
    ```
    To run pre-commit hooks on all files manually, run:
    ```sh
    poetry run pre-commit run --all-files
    ```

- GitHub Actions: This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml` and runs tests on every push to the `main` branch.



### Tests
To run the tests, simply run `poetry run pytest`. <br/>
Note that some of the tests are live tests that actually download a file from GCS bucket. Depending on your system and internet speed, it might take upto few seconds to execute the tests.


## Improvements

There is some scope of improvements to further enhance the performance

 - __Parallel Processing__: Since we would be potentially dealing with hundreds of files, we can spped up the process significantly by using parallel processing.

 - __Object Oriented Programming__: For better maintainability, we should refactor the code to use OOP (perhaps rewrite using SOLID design principles).

 - __Bloated with dependencies__: Currently, this has some heavy dependencies. To have something light weight, we can narrow down the exact functionalities needed and look for some light-weight libraries.

 - __Tests and Coverage Report__: Add some more end to end tests (including for one when this is being used as a library) and add coverage report.


### Fix:
There are some minor issues that need to be fixed:

 - When this is being used as a library in a python environment, GCS gets initialized when it is imported. This is not the desired behaviour. However, this should be an easy fix.

 - When this is used as a container, it proceeds to open the file remotely and then suddenly dies without any error. This needs to be fixed.

 - There are some conflicts with `black` and `flake8`'s formatting. These conflicts need to be fixed.
