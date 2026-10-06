# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = df.copy()
    df = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {len(before)} -> {len(df)} rows")
    return df


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    before = df.copy()
    if axis != "rows" and axis != "columns":
        logger.error(f"ValueError: {axis} is an unsupported axis. "
                      "Supported values are 'rows' and 'columns.'")
        raise ValueError
    if axis == "rows":
        df = df.dropna()
    elif axis == "columns":
        df = df.dropna(axis=1)
    logger.debug(f"handle_missing: {len(before)} -> {len(df)} rows")    
    return df

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    before = df.copy()
    if method != "iqr" and method != "zscore":
        logger.error(f"ValueError: {method} is an unsupported method. "
                        "Supported values are 'iqr' and 'zscore.'")
        raise ValueError
    if method == "iqr":
        for column in columns:
            if column not in df.columns:
                logger.warning(f"{column} does not exist")
                return df
            elif not pd.api.types.is_numeric_dtype(df[column]):
                logger.warning(f"{column} is not numeric")
                return df
            else:
                q1 = df[column].quantile(0.25)
                q3 = df[column].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - threshold * iqr
                upper = q3 + threshold * iqr
                df_cleaned = df[(df[column] >= lower) & (df[column] <= upper)]
    elif method == "zscore":
        for column in columns:
            if column not in df.columns:
                logger.warning(f"{column} does not exist")
                return df
            elif not pd.api.types.is_numeric_dtype(df[column]):
                logger.warning(f"{column} is not numeric")
                return df
            else:
                mu = df[column].mean()
                std = df[column].std()
                z_scores = (df[column] - mu) / std
                df_cleaned = df[z_scores.abs() < threshold]
    logger.debug(f"{column}: method={method}, threshold ={threshold}," 
                 f"removed={len(before) - len(df_cleaned)}")
    return df_cleaned

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    # Duplicates
    duplicates = config["processing"]["remove_duplicates"]
    if duplicates:
        df = remove_duplicates(df)

    # Missing values
    missing = config["processing"]["missing"]["enabled"]
    axis = config["processing"]["missing"]["axis"]
    if missing:
        df = handle_missing(df, axis=axis)

    # Outliers
    outliers = config["processing"]["outliers"]["enabled"]
    columns = config["processing"]["outliers"]["columns"]
    method = config["processing"]["outliers"]["method"]
    threshold = config["processing"]["outliers"]["threshold"]
    if outliers:
        df = remove_outliers(df, columns=columns, method=method, threshold=threshold)

    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    report = {"rows_before": len(df_before),
              "rows_after": len(df_after),
              "rows_removed": len(df_before) - len(df_after),
              "columns_before": len(df_before.columns),
              "columns_after": len(df_after.columns),
              "columns_removed": len(df_before.columns) - len(df_after.columns),
              }
    return report
