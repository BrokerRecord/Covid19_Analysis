# COVID-19 Data Analysis Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-orange)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive data analysis project exploring global COVID-19 trends, patterns, and insights using data from Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE).

## 📊 Project Overview

This project provides a complete pipeline for COVID-19 data analysis, from data acquisition to visualization and insights generation. It includes automated data collection, preprocessing, exploratory analysis, time series analysis, and interactive visualizations.

## 🚀 Features

- **Automated Data Collection**: Daily updates from JHU CSSE COVID-19 repository
- **Data Preprocessing**: Cleaning, transformation, and merging of global datasets
- **Exploratory Data Analysis**: Statistical summaries and trend analysis
- **Time Series Analysis**: Growth patterns, moving averages, and forecasting insights
- **Interactive Visualizations**: Charts, heatmaps, and global distribution maps
- **Top Countries Analysis**: Ranking by cases, deaths, and mortality rates
- **Modular Architecture**: Reusable and extensible code structure

## 📁 Project Structure

```
covid19-analysis/
│
├── 📁 notebooks/                          # Jupyter notebooks for analysis
│   ├── 01_exploratory_analysis.ipynb     # Initial data exploration
│   └── 02_time_series_analysis.ipynb     # Time series and trend analysis
│
├── 📁 src/                               # Python source code
│   ├── __init__.py
│   ├── data_loader.py                   # Data download and preprocessing
│   ├── analysis.py                      # Analytical functions and calculations
│   └── visualization.py                 # Plotting and visualization utilities
│
├── 📁 data/                             # Data storage
│   ├── 📁 raw/                          # Original downloaded data
│   └── 📁 processed/                    # Cleaned and processed data
│
├── requirements.txt                     # Python dependencies
├── run_analysis.py                      # Main execution script
└── README.md                           # Project documentation
```

## 🛠 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd covid19-analysis
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Data

```bash
python run_analysis.py
```

Or manually download data:

```python
from src.data_loader import CovidDataLoader
loader = CovidDataLoader()
loader.download_data()
```

## 📈 Usage

### Quick Start

Run the complete analysis pipeline:

```bash
python run_analysis.py
```

### Jupyter Notebooks

For interactive analysis:

```bash
jupyter notebook
```

Then open and run:

1. `notebooks/01_exploratory_analysis.ipynb` - Initial data exploration
2. `notebooks/02_time_series_analysis.ipynb` - Time series analysis

### Manual Analysis

```python
import sys
sys.path.append('./src')

from data_loader import CovidDataLoader
from analysis import CovidAnalysis
from visualization import CovidVisualizer

# Load data
loader = CovidDataLoader()
raw_data = loader.load_data()
processed_data = loader.preprocess_data(raw_data)
merged_data = loader.get_merged_data(processed_data)

# Analyze
analyzer = CovidAnalysis(merged_data)
visualizer = CovidVisualizer()

# Get insights
top_countries = analyzer.get_top_countries_by_cases(10)
global_summary = analyzer.get_global_summary()

# Create visualizations
fig = visualizer.plot_top_countries(top_countries)
plt.show()
```

## 🔍 Analysis Features

### 1. Global Summary Statistics

- Total confirmed cases, deaths, and recoveries
- Global mortality and recovery rates
- Country-level comparisons
- Active cases tracking

### 2. Top Countries Analysis

- Top 10 countries by confirmed cases
- Top 10 countries by death rates (with minimum cases filter)
- Growth trend comparisons
- Regional hotspot identification

### 3. Time Series Analysis

- Daily and cumulative trends
- Growth rate calculations (daily and weekly)
- 7-day moving averages
- Country-specific progression patterns

### 4. Visualizations

- **Bar Charts**: Top countries by various metrics
- **Line Plots**: Time series trends and growth rates
- **Heatmaps**: Case distribution across countries and time
- **Interactive Maps**: Global COVID-19 distribution
- **Comparative Analysis**: Multiple country comparisons

## 📊 Example Outputs

### Global Summary

```
Global COVID-19 Summary:
  Total_Confirmed: 676,609,955
  Total_Deaths: 6,881,955
  Total_Recovered: 652,201,715
  Total_Active: 17,526,285
  Global_Death_Rate: 1.02%
  Number_of_Countries: 191
```

### Top Countries Analysis

```
Top 10 Countries by Confirmed Cases:
  United States: 103,436,829
  India: 44,679,011
  France: 39,752,321
  Germany: 38,237,276
  Brazil: 37,196,511
  Japan: 33,803,572
  South Korea: 31,792,044
  Italy: 25,903,041
  United Kingdom: 24,603,076
  Russia: 23,044,621
```

## 🗃 Dataset Information

### Source

- **Provider**: Johns Hopkins University Center for Systems Science and Engineering
- **Repository**: [JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19)
- **Update Frequency**: Daily
- **License**: CC BY 4.0

### Data Types

- **Confirmed Cases**: Total confirmed COVID-19 cases
- **Deaths**: Total deaths attributed to COVID-19
- **Recovered**: Total recovered cases (where available)
- **Geographic Coverage**: Global, country-level data

## 🎯 Key Insights

This analysis helps answer important questions:

- Which countries were most affected by COVID-19?
- How did case growth rates vary across different regions?
- What were the mortality rates and how did they evolve over time?
- Which countries had the most effective pandemic responses?
- What were the global spread patterns and hotspots?

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests for:

- New analysis methods and visualizations
- Improved data processing pipelines
- Additional machine learning models for forecasting
- Enhanced documentation and examples
- Bug fixes and performance improvements

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-analysis`
3. Commit changes: `git commit -am 'Add new analysis method'`
4. Push to branch: `git push origin feature/new-analysis`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The COVID-19 data is sourced from JHU CSSE and is available under the Creative Commons Attribution 4.0 International License.

## 🙏 Acknowledgments

- Johns Hopkins University Center for Systems Science and Engineering for maintaining the COVID-19 data repository
- The global research community for their contributions to pandemic data collection and analysis
- Contributors and maintainers of the Python data science ecosystem

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/covid19-analysis/issues) page
2. Create a new issue with detailed description
3. Provide your environment details and error messages

## 🔄 Updates

This project is maintained and updated regularly:

- Data updates: Daily automatic downloads available
- Code improvements: Continuous integration and testing
- Feature additions: Based on community feedback and research needs

---
