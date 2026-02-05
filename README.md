# DeGiro Portfolio Analyzer

DeGiro Portfolio Analyzer is a Python-based application designed to compare two different DeGiro portfolio snapshots. It helps investors track wealth changes and calculate market performance while isolating the impact of deposits and withdrawals. Just export two csv's out of DeGiro and insert them in the application. The application has not been tested with csv's from other brokers.

## Features

* **Snapshot comparison**: Load two CSV exports from DeGiro to see how individual positions have changed over time.
* **Performance metrics**: Automatically calculates **Wealth Change** (absolute Euro value) and **Market Performance** (percentage change based on stock price).
* **Weighted returns**: Provides a weighted average market return that excludes the noise of new deposits or withdrawals.
* **Data export**: Save your analysis to a CSV file.
* **Sorting**: Interactive table allows sorting by market performance to quickly identify your best and worst performers.


## Usage

See the Releases section to download the executable for Windows or MacOS. Your OS might complain about installing unknown applications, but the beauty of open source is that you can inspect the code yourself.

If you'd like to build from source, you will need:

* **Python 3.x**
* **pandas**
* **numpy**
* **tkinter** (usually included with standard Python installations)
