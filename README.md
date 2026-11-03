Data Cleaner Pro

Data Cleaner Pro is an interactive Python application for analyzing,
visualizing and cleaning CSV and Excel datasets.

The application is built with Python, Pandas and Streamlit.

## Features

### File Upload

- CSV support
- Excel support
- Interactive data preview

### Dataset Analysis

- Row count
- Column count
- Duplicate detection
- Missing value detection
- Missing value percentages
- Automatic column type detection

### Statistics

- Mean
- Median
- Standard deviation
- Minimum
- Maximum
- Quartiles

### Correlation Analysis

Automatically calculates correlations between numeric columns.

### Data Visualization

The application includes:

- Histograms
- Bar charts
- Line charts
- Scatter plots

### Data Cleaning

Users can:

- Remove duplicate rows
- Trim text values
- Remove selected columns
- Fill numeric missing values using mean
- Fill numeric missing values using median
- Fill categorical missing values using mode
- Drop rows containing missing values
- Keep missing values unchanged

### Before vs After

The application compares the original dataset with the cleaned dataset.

It displays:

- Rows
- Columns
- Duplicate values
- Missing values

### Export

Cleaned datasets can be downloaded as:

- CSV
- Excel

The application also generates a cleaning report.

## Technologies

- Python
- Pandas
- NumPy
- Streamlit
- OpenPyXL

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL

Enter the project directory:

cd data-cleaner-pro

Create a virtual environment:

python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\activate

Install dependencies:

python -m pip install -r requirements.txt

Run

Start the application:

python -m streamlit run app.py

Then open:
http://localhost:8501
Project Structure
data-cleaner-pro/
│
├── app.py
├── analyzer.py
├── cleaner.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── sample_data/
Purpose

This project demonstrates practical Python skills in:

    Data processing
    Data cleaning
    Data analysis
    Data visualization
    File handling
    Modular programming
    Interactive application development