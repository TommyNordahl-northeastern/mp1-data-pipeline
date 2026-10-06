"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    # valid input
    python3 pipeline.py --input data/sales.csv --output clean.csv 
    
    # valid input with extra settings
    python3 pipeline.py --input data/sales.csv --output results.json --format json --verbose

    # not valid input, should mention issues at ERROR level
    python3 pipeline.py --input data.csv --output clean.csv
"""

import argparse
import logging
import sys
from pathlib import Path
from src import(
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input
)

logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description= "Parse arguments"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
            "--config", "-c",
            default="config.yaml",
            help="Config file (yaml)"
        )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed DEBUG messages"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments() # parse the command line arguments
    setup_logging(args.verbose) # setup loggin with verbose

    # log arguments parsed at the DEBUG level
    logger.debug(f"Arguments parsed: input='{args.input}', " \
                 f"output='{args.output}', " \
                 f"verbose={args.verbose}")

    # validate input and config files from command line, exit if either are false
    input_bool = validate_input(args.input)
    config_bool = validate_input(args.config)
    if not input_bool or not config_bool:
        sys.exit(1)

    # try to load data from input and config files, excepting ValueError
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # save a copy of original data
    data_original = data.copy()

    required_cols = config["validation"]["required_columns"]
    numeric_cols = config["validation"]["numeric_columns"]
    try:
        data = validate_dataframe(df=data, required_columns=required_cols, numeric_columns=numeric_cols)
        logger.info(f"{len(data_original) - len(data)} rows removed through numeric validation. All required columns present.")
    except ValueError:
        sys.exit(1)

    data_original = data.copy()

    # use process_data with config settings within a try block
    try:
        data = process_data(df=data, config=config)
    except ValueError:
        sys.exit(1)

    # create and log cleaning report
    report = create_cleaning_report(df_before=data_original, df_after=data)
    logger.info(f"Processing complete: {report["rows_before"]} -> {report["rows_after"]}")

    # write data to the output csv
    save_data(data, args.output)
    logger.info(f"Saved cleaned data to {args.output}")
    
    # print full cleaning report
    print(f"\n Cleaning report:\n {report}")

if __name__ == "__main__":
    main()