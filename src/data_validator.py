# src/data_validator.py
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    df_original = df.copy()
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"{col} not in given dataframe")
            raise ValueError
        
    for col in numeric_columns:
        df_before = df.copy()
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    invalid_rows.append(i)
        # : Remove the invalid rows.
        for row in invalid_rows:
            df = df.drop(row)
        if len(df_before) != len(df):
            logger.debug(f"Removed {len(df_before) - len(df)} rows with invalid numeric values in {col}")
        
        #convert to a numeric data type
        df[col] = pd.to_numeric(df[col])
    logger.debug(f"Validation complete: {len(df_original)} -> {len(df)}.")
    return df