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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


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
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )
    parser.add_argument(
        "--format", 
        default="csv",
        choices=["csv", "json"],
        help="Output format: csv or json, default is csv"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed DEBUG messages"
    )
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    p = Path(filepath)
    if not p.is_file():
        logger.error(f"Input file not found: '{filepath}'")
        return False
    else:
        logger.info(f"Input file validated: '{filepath}'")
        return True


def main():
    """Main pipeline function."""
    args = parse_arguments() # 1. parse the command line arguments
    setup_logging(args.verbose) # 2. setup loggin with verbose

    logger.debug(f"Arguments parsed: input='{args.input}', " \
                 f"output='{args.output}', format='{args.format}', " \
                 f"verbose={args.verbose}") # 3. Log the parsed arguments (DEBUG)
    input_bool = validate_input(args.input)
    if not input_bool:
        sys.exit(1)
        
    

if __name__ == "__main__":
    main()