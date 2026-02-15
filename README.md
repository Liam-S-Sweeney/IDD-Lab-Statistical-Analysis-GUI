## Project: IDD Lab Statistical Analysis GUI

A Python-based GUI analysis tool developed to support exploratory and multivariate statistical workflows for large behavioral research datasets. The application abstracts common statistical tasks into an interactive GUI, allowing researchers to rapidly explore variables, generate descriptive summaries, and visualize relationships without writing repetitive analysis scripts.

### Key Capabilities
- Dynamic, searchable dropdowns for variable selection
- Support for multi-variable exploratory workflows
- Automated computation of descriptive statistics:
  - Central tendency (mean, median, mode)
  - Variability (variance, standard deviation, IQR)
  - Distribution shape (skewness, kurtosis)
  - Frequency and count metrics
- Missing-data handling via sentinel value conversion
- CSV export for reproducible downstream analysis

### Multivariate & Correlational Analysis
- Pairwise scatterplots, density plots, and regression overlays
- Correlation matrices and heatmaps for identifying linear relationships and multicollinearity
- Designed for early-stage hypothesis generation and feature exploration

### Technical Highlights
- Built with Python, Tkinter, pandas, NumPy, seaborn, and matplotlib
- Object-oriented GUI components for scalable widget management
- Vectorized pandas operations to avoid slow Python loops
- Defensive input validation to prevent runtime dataframe errors
- Modular analysis functions for extensibility

### Motivation
Research workflows often require repeated, one-off statistical scripts for basic exploration tasks. This tool was developed to reduce that overhead, improve reproducibility, and allow researchers to focus on interpretation rather than implementation.

### Intended Use
- Behavioral and clinical research datasets
- Longitudinal survey data
- Exploratory data analysis prior to modeling
- Internal lab tooling for research assistants and graduate students
