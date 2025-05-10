"""
Holiday Features Module

This module provides functions to add holiday-related features to pandas DataFrames.
"""

import pandas as pd
from typing import List, Optional, Union
import ast
from pathlib import Path
import os
import importlib.resources as pkg_resources
import importlib.util
import importlib.metadata
import io
import sys

# Constants
VALID_COUNTRIES = ['ES', 'IT']
SPAIN_COUNTIES = [
    'ES-AN', 'ES-AR', 'ES-AS', 'ES-CB', 'ES-CE', 'ES-CL', 'ES-CM', 'ES-CN',
    'ES-CT', 'ES-EX', 'ES-GA', 'ES-IB', 'ES-MC', 'ES-MD', 'ES-ML', 'ES-NC',
    'ES-PV', 'ES-RI', 'ES-VC'
]

def _load_holiday_data(country_code: str) -> pd.DataFrame:
    """
    Load holiday data for a specific country.
    
    Parameters
    ----------
    country_code : str
        The country code ('ES' for Spain, 'IT' for Italy)
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing holiday information
    
    Raises
    ------
    ValueError
        If country_code is not supported
    FileNotFoundError
        If holiday data file is not found
    """
    if country_code not in VALID_COUNTRIES:
        raise ValueError(f"Country code {country_code} not supported. Valid codes: {VALID_COUNTRIES}")
    
    if country_code == 'ES':
        # Debug info
        package_name = "orama_utils"
        file_name = "spain_holidays.csv"
        
        try:
            # For Python 3.9+
            if sys.version_info >= (3, 9):
                try:
                    with pkg_resources.files("orama_utils").joinpath("db", file_name).open("rb") as f:
                        holidays_df = pd.read_csv(f)
                        return _process_holidays_df(holidays_df)
                except Exception as e:
                    print(f"Method 1 failed: {e}")
            
            # For Python 3.7-3.8
            try:
                with pkg_resources.path("orama_utils.db", file_name) as path:
                    holidays_df = pd.read_csv(path)
                    return _process_holidays_df(holidays_df)
            except Exception as e:
                print(f"Method 2 failed: {e}")
            
            # Try using resource_string approach
            try:
                csv_data = pkg_resources.read_binary("orama_utils.db", file_name)
                holidays_df = pd.read_csv(io.BytesIO(csv_data))
                return _process_holidays_df(holidays_df)
            except Exception as e:
                print(f"Method 3 failed: {e}")
                
            # Try direct path to orama_utils package
            try:
                import orama_utils
                base_path = os.path.dirname(os.path.abspath(orama_utils.__file__))
                file_path = os.path.join(base_path, "db", file_name)
                holidays_df = pd.read_csv(file_path)
                return _process_holidays_df(holidays_df)
            except Exception as e:
                print(f"Method 4 failed: {e}")
                
            # Last resort: check current working directory and its parent
            try:
                # Try in the current directory
                current_dir = os.getcwd()
                file_path = os.path.join(current_dir, "db", file_name)
                if os.path.exists(file_path):
                    holidays_df = pd.read_csv(file_path)
                    return _process_holidays_df(holidays_df)
                
                # Try in parent directory 
                parent_dir = os.path.dirname(current_dir)
                file_path = os.path.join(parent_dir, "db", file_name)
                if os.path.exists(file_path):
                    holidays_df = pd.read_csv(file_path)
                    return _process_holidays_df(holidays_df)
                    
                # Failed to load from any location
                raise FileNotFoundError(f"Could not find holiday data file at any location")
            except Exception as e:
                print(f"Method 5 failed: {e}")
                
            raise FileNotFoundError(f"All methods to load holiday data file failed")
                
        except Exception as e:
            raise FileNotFoundError(f"Error loading holiday data: {e}")
    else:  # IT
        # TODO: Implement Italy holidays when available
        return pd.DataFrame(columns=['date', 'global', 'counties'])

def _process_holidays_df(holidays_df):
    """Process the loaded holiday dataframe to convert string columns to proper types."""
    holidays_df['counties'] = holidays_df['counties'].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) and x != '' else []
    )
    return holidays_df

def add_holiday_features(
    df: pd.DataFrame,
    date_column: str = 'date',
    country_column: str = 'country',
    county_column: str = 'county',
    county_threshold: int = 3
) -> pd.DataFrame:
    """
    Add holiday-related features to a pandas DataFrame based on date, country, and county information.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing date and country information
    date_column : str, default='date'
        Name of the column containing datetime values
    country_column : str, default='country'
        Name of the column containing country codes
    county_column : str, default='county'
        Name of the column containing county codes
    county_threshold : int, default=3
        Number of counties threshold for many_counties_holiday flag
    
    Returns
    -------
    pd.DataFrame
        DataFrame with added holiday features:
        - is_public_holiday: True if the date is a global holiday
        - is_local_holiday: True if the date is a holiday for the specific county
        - many_counties_holiday: True if more than county_threshold counties celebrate that holiday
        - is_day_before_holiday: True if the next day is a public or local holiday
        - is_day_after_holiday: True if the previous day is a public or local holiday
    
    Raises
    ------
    ValueError
        If required columns are missing or contain invalid values
    """
    # Input validation
    if date_column not in df.columns:
        raise ValueError(f"Date column '{date_column}' not found in DataFrame")
    if country_column not in df.columns:
        raise ValueError(f"Country column '{country_column}' not found in DataFrame")
    if county_column and county_column not in df.columns:
        raise ValueError(f"County column '{county_column}' not found in DataFrame")
    if county_threshold < 1:
        raise ValueError("county_threshold must be a positive integer")
    
    # Make a copy to avoid modifying the input DataFrame
    result_df = df.copy()
    
    # Ensure date column is datetime
    result_df[date_column] = pd.to_datetime(result_df[date_column])
    
    # Validate country codes
    invalid_countries = set(result_df[country_column].unique()) - set(VALID_COUNTRIES)
    if invalid_countries:
        raise ValueError(f"Invalid country codes found: {invalid_countries}. Valid codes: {VALID_COUNTRIES}")
    
    # Initialize holiday columns
    result_df['is_public_holiday'] = False
    result_df['is_local_holiday'] = False
    result_df['many_counties_holiday'] = False
    result_df['is_day_before_holiday'] = False
    result_df['is_day_after_holiday'] = False
    
    # Process each country separately
    for country in VALID_COUNTRIES:
        country_mask = result_df[country_column] == country
        if not country_mask.any():
            continue
            
        holidays_df = _load_holiday_data(country)
        
        # Convert holiday dates to datetime for comparison
        holidays_df['date'] = pd.to_datetime(holidays_df['date'])
        
        # First pass: set the basic holiday flags
        for _, holiday in holidays_df.iterrows():
            date_mask = result_df[date_column].dt.date == holiday['date'].date()
            combined_mask = country_mask & date_mask
            
            if not combined_mask.any():
                continue
            
            # Set public holiday flag
            is_public = holiday.get('global', False)
            if is_public:
                result_df.loc[combined_mask, 'is_public_holiday'] = True
            
            # Set local holiday flag if county matches
            counties = holiday.get('counties', [])
            if counties:
                local_mask = result_df[county_column].isin(counties)
                local_combined_mask = combined_mask & local_mask
                if local_combined_mask.any():
                    result_df.loc[local_combined_mask, 'is_local_holiday'] = True
            
            # Set many counties flag based on threshold
            if len(counties) > county_threshold:
                result_df.loc[combined_mask, 'many_counties_holiday'] = True
        
        # Second pass: set day before/after flags based on public/local holidays
        for index, row in result_df[country_mask].iterrows():
            current_date = row[date_column].date()
            
            # Check if day after is a holiday
            next_day = current_date + pd.Timedelta(days=1)
            next_day_mask = (result_df[date_column].dt.date == next_day) & country_mask
            
            if next_day_mask.any():
                next_day_rows = result_df[next_day_mask]
                # Check if any next day row has public or local holiday
                if (next_day_rows['is_public_holiday'].any() or 
                    next_day_rows['is_local_holiday'].any()):
                    result_df.loc[index, 'is_day_before_holiday'] = True
            
            # Check if day before is a holiday
            prev_day = current_date - pd.Timedelta(days=1)
            prev_day_mask = (result_df[date_column].dt.date == prev_day) & country_mask
            
            if prev_day_mask.any():
                prev_day_rows = result_df[prev_day_mask]
                # Check if any previous day row has public or local holiday
                if (prev_day_rows['is_public_holiday'].any() or 
                    prev_day_rows['is_local_holiday'].any()):
                    result_df.loc[index, 'is_day_after_holiday'] = True
    
    return result_df
