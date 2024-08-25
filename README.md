# Data Transformation pipeline: NetCDF to Parquet


### Task
This pipeline transforms total precipitation NetCDF files into Parquet format. <br/>
The source data is publicly available and is hosted at `gs://gcp-public-data-arco-era5/raw/date-variable-single_level`.

The transformed data supports:
 - regular queries with filtering with timestamp.
 - filtering by H3 geospatial index

## Installation

### Using Docker
To build the docker image, run:
```sh
docker build -t data_transformations .
```

To run the docker container, here's an example command:
`docker run -v $(pwd)/output:/app/output data_transformations <start_date> <end_date> <out_dir>`
<br/>
Here, `start_date` and `end_date` are in DD-MM-YYYY format. 
<br/>
And `out_dir` is the directory where the parquet files will be generated. 

For example:
```sh
docker run -v $(pwd)/output:/app/output data_transformations 01-01-2022 04-01-2022 out_dir
```

### Using Poetry
Poetry makes life easier for managing dependencies and creating environments. Note that you need to have Poetry pre-installed in your system. To install Poetry, follow the steps listed [here](https://python-poetry.org/docs/#installation).

To generate and activate the environment, run following commands from the root directory:
```sh
poetry install
poetry shell
python -m data_transformations 01-01-2023 03-01-2023 ./parquet_files
```

### Using pip
..


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

## TODOs
 - add queries
 - add visual examples in readme
 - add streamlit?
 - Package it into a library
 - add coverage report?
 - add doc strings
 - fix black and flake8 conflict

## Improvements
 - speed up
 - OOP

