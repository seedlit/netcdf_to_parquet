# Data Transformation pipeline: NetCDF to Parquet


### Task
This pipeline transforms total precipitation NetCDF files into Parquet format. <br/>
The source data is publicly available and is hosted at `gs://gcp-public-data-arco-era5/raw/date-variable-single_level`.

The transformed data supports:
 - regular queries with filtering with timestamp.
 - filtering by H3 geospatial index

## How to run
### TODO: update instructions
Build the Docker image
`docker build -t data_transformation .`

Run the Docker container
`docker run -v $(pwd)/output:/app/output data_transformation 01-01-2022 02-01-2022 out_dir`

### Features
 - Poetry for dependency management - Poetry makes life easier for managing dependencies and creating environments. To setup a virtual environment, simply run `poetry install` from the root directory. It will create a virtual environment for you. To spawn a shell, run `poetry shell`. Note that you need to have Poetry pre-installed in your system. To install Poetry, follow the steps listed [here](https://python-poetry.org/docs/#installation).

 - To avoid saving the source file locally, this project uses [gcsfs](https://github.com/fsspec/gcsfs) to stream the source NetCDF file into memory.

 - Pre-commit Hooks: This project uses pre-commit hooks to ensure code quality. To set up pre-commit hooks, run:

    ```sh
    poetry run pre-commit install
    ```
    To run pre-commit hooks on all files manually, run:
    ```sh
    poetry run pre-commit run --all-files
    ```

- GitHub Actions: This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml` and runs tests on every push to the `master` branch.



### Tests
To run the tests, simply run `poetry run pytest`. <br/>
Note that some of the tests are live tests that actually download a file from GCS bucket. Depending on your system and internet speed, it might take upto few seconds to execute the tests.

## TODOs
 - add dockerfile
 - add container
 - add visual examples in readme
 - add streamlit?
 - how to speed up?
 - OOP?
 - Package it into a library
 - setup GitHub actions
 - add coverage report?
 - add doc strings
 - add exception handling and logs
 - add tqdm or some other progress bar

## Improvements
