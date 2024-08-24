# Jua Data Engineer Assignment


### Task
Create a pipeline for transforming 2022 total precipitation NetCDF files into Parquet format. <br/>
The source data is publicly available and is hosted at `gs://gcp-public-data-arco-era5/raw/date-variable-single_level`.

### Requirements
 - The transformed data should support regular queries with filtering with timestamp.
 - The transformed data should support filtering by H3 geospatial index

<br/><br/>
# Solution
The solution has been implemented in python.

### Features
 - Poetry for dependency management - Poetry makes life easier for managing dependencies and creating environments. To setup a virtual environment, simply run `poetry install` from the root directory. It will create a virtual environment for you. To spawn a shell, run `poetry shell`. Note that you need to have Poetry pre-installed in your system. To install Poetry, follow the steps listed [here](https://python-poetry.org/docs/#installation).

 - To avoid saving the source file locally, this project uses [gcsfs](https://github.com/fsspec/gcsfs) to stream the source NetCDF file into memory.

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
