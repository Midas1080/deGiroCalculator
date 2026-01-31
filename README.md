# DeGiro Portfolio Analyzer

DeGiro Portfolio Analyzer is a Python-based desktop application designed to compare two different DeGiro portfolio snapshots. It helps investors track wealth changes and calculate market performance while isolating the impact of deposits and withdrawals.

## Features

* **Snapshot Comparison**: Load two CSV exports from DeGiro to see how individual positions have changed over time.
* **Performance Metrics**: Automatically calculates **Wealth Change** (absolute Euro value) and **Market Performance** (percentage change based on stock price).
* **Weighted Returns**: Provides a weighted average market return that excludes the noise of new deposits or withdrawals.
* **Data Export**: Save your analysis to a CSV file optimized for European Excel settings (using semicolon delimiters).
* **Sorting**: Interactive table allows sorting by market performance to quickly identify your best and worst performers.


## Requirements

If you'd like to build from source, you will need:

* **Python 3.x**
* **pandas**
* **tkinter** (usually included with standard Python installations)


## Installation and Usage

### Running from Source
See Releases sction to download the executable
