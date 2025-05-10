# Orama Utils

A collection of utility functions for data processing and feature engineering.

## Features

- **Date feature generation**: Add time-based features to your DataFrame
- **Holiday feature generation**: Add holiday information based on country and region
- **Weather feature generation**: (Coming soon)

## Installation

You can install the package using pip:

```bash
pip install orama-utils
```

For development installation:

```bash
git clone https://github.com/Orama-Solutions/utils.git
cd utils
pip install -e .[dev]
```

## Usage

### Date Features

Add date-related features to your DataFrame:

```python
import pandas as pd
from orama_utils import add_date_features

# Create your DataFrame
df = pd.DataFrame({
    'date': ['2023-01-01', '2023-12-25'],
    'value': [100, 200]
})

# Add all available date features
result = add_date_features(df, date_column='date')

# Add only specific features
selected_features = ['year', 'month', 'week_of_month', 'is_monday', 'is_weekend', 'season']
result = add_date_features(df, date_column='date', features=selected_features)
```

#### Available Date Features

- Basic Components: `year`, `month`, `day`, `week_of_month`, `week_of_year`, `quarter`
- Day of Week Flags: `is_monday`, `is_tuesday`, `is_wednesday`, `is_thursday`, `is_friday`, `is_saturday`, `is_sunday`, `is_weekend`
- Calendar Flags: `is_month_start`, `is_month_end`, `is_quarter_start`, `is_quarter_end`, `is_year_start`, `is_year_end`
- Season: `season` (1=Winter, 2=Spring, 3=Summer, 4=Fall for Northern Hemisphere)

### Holiday Features

Add holiday-related features to your DataFrame:

```python
import pandas as pd
from orama_utils import add_holiday_features

# Create your DataFrame
df = pd.DataFrame({
    'date': ['2023-01-01', '2023-12-25'],
    'country': ['ES', 'ES'],
    'county': ['ES-MD', 'ES-CT']
})

# Add holiday features with default threshold (3 counties)
result = add_holiday_features(df)

# With custom county threshold
result = add_holiday_features(df, county_threshold=5)

# With custom column names
result = add_holiday_features(
    df,
    date_column='date',
    country_column='country_code',
    county_column='region_code'
)
```

#### Available Holiday Features

The function adds the following columns:
- `is_public_holiday`: True for national holidays
- `is_local_holiday`: True for county-specific holidays
- `many_counties_holiday`: True when multiple counties celebrate the holiday (more than the specified threshold)
- `is_day_before_holiday`: True if the next day is a public or local holiday
- `is_day_after_holiday`: True if the previous day is a public or local holiday

#### Supported Countries

Currently supported countries:
- `ES`: Spain (with county-level holiday information)
- `IT`: Italy (basic support, county-level information coming soon)

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Updating the Package Version

When releasing a new version of the package, you need to update the version number in three places:

1. In `pyproject.toml`:
   ```toml
   [project]
   name = "orama-utils"
   version = "0.1.1"  # Update this
   ```

2. In `setup.py`:
   ```python
   setup(
       name="orama-utils",
       version="0.1.1",  # Update this
       # ...
   )
   ```

3. In `orama_utils/__init__.py`:
   ```python
   __version__ = '0.1.1'  # Update this
   ```

Make sure to update all three files with the same version number to avoid build inconsistencies.

#### Building the Package

To build the package:

**Windows:**
```powershell
# Clean previous builds
Remove-Item -Path dist\* -Force -ErrorAction SilentlyContinue
Remove-Item -Path *.egg-info -Recurse -Force -ErrorAction SilentlyContinue

# Build new package
python -m build
```

**macOS/Linux:**
```bash
# Clean previous builds
rm -rf dist/* *.egg-info/

# Build new package
python -m build
```

The build output will be in the `dist/` directory:
- `orama_utils-x.y.z-py3-none-any.whl` (wheel)
- `orama_utils-x.y.z.tar.gz` (source distribution)

#### Publishing to PyPI

First, ensure you have configured your PyPI credentials in `~/.pypirc` or as environment variables.

**Windows/macOS/Linux:**
```bash
# Upload to PyPI
python -m twine upload dist/*
```

For test uploads, use TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

### Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.