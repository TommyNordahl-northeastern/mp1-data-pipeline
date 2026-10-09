This project was completed for my DS3500 course, Advanced Programming with Data, in October 2026. We started with developing a simple command line data pipeline that parse basic command line arguments like input and output. Each subsequent update added more modules that could load, process, and validate data. This culminated in creating an src/ folder with all of the support modules included. These modules were then installed as a package that was installed into pipeline.py, the main file, with a convenient __init__.py file in src/. 

This program uses a yaml config file that decides exactly how the data given in the input file is processed. Processing involves removing outliers, rows (or columns) with empty entries, and validating that required columns exist and certain columns contain numeric values. A filepath for the config file is given with the command line arguments, as well as a path to follow for the output with the saved data.

An example of a command that works with pipeline.py:
python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

This command gives an input file, and output file, a config file, and calls for the whole program to be run with the DEBUG setting for logging (due to --verbose). The output given for this command is below. Note that the data is actually saved to output/clean.csv and that the files given must exist to not raise errors:

16:24:07 DEBUG    __main__ - Arguments parsed: input='fixtures/sample_data.csv', output='output/clean.csv', verbose=True
16:24:07 INFO     src.utils - Input file validated: 'fixtures/sample_data.csv'
16:24:07 INFO     src.utils - Input file validated: 'config/config.yaml'
16:24:07 INFO     src.data_loaders - Loaded CSV File: fixtures/sample_data.csv (100 rows)
16:24:07 INFO     src.data_loaders - Loaded a YAML File: config/config.yaml
16:24:07 DEBUG    src.data_validator - Removed 2 rows with invalid numeric values in rating
16:24:07 DEBUG    src.data_validator - Validation complete: 100 -> 98.
16:24:07 INFO     __main__ - 2 rows removed through numeric validation. All required columns present.
16:24:07 DEBUG    src.data_processor - remove_duplicates: 98 -> 96 rows
16:24:07 DEBUG    src.data_processor - handle_missing: 96 -> 94 rows
16:24:07 DEBUG    src.data_processor - rating: method=iqr, threshold =1.5,removed=2
16:24:07 INFO     __main__ - Processing complete: 98 -> 92
16:24:07 DEBUG    src.data_output - 92 rows saved to output/clean.csv
16:24:07 INFO     __main__ - Saved cleaned data to output/clean.csv

 Cleaning report:
 {'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}

 ## Note that the cleaning report starts "rows_before" after the file is validated, so the rows removed due to duplicates, misisng, and rating are accounted for, but not rows removed due to missing numeric values from src.data_validator.