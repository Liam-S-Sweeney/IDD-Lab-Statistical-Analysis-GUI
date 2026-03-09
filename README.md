# IDD Lab Data Analysis Tool

A desktop GUI application for exploratory data analysis of longitudinal neurobehavioral data. Built for research teams who need quick descriptive statistics, visualizations, and correlation analyses without writing code.

---

## Features

- **Single-variable descriptives** — mean, median, mode, variance, std, range, IQR, skewness, kurtosis, SE, frequency tables, and more
- **Multivariate exploration** — per-variable distribution plots (probability plot, histogram with normal fit, box, violin, swarm)
- **Multivariate visualization** — pair grid with scatter, KDE, and histogram panels; supports hue and size encoding
- **Correlational analysis** — correlation heatmap + pairplot with regression lines
- **Batch CSV generation** — master descriptives CSV for all variables, or one CSV per variable

---

## Project Structure

```
├── main_gui.py                      # Entry point — launches the Tkinter GUI
├── config.py                        # Paths, missing codes, and plot defaults
├── data_loader.py                   # CSV loading and cleaning utilities
├── cdfs.py                          # Core descriptive statistics computation
├── global_descriptive_generator.py  # Batch CSV generators
├── multivariate_exploration.py      # Plotting and correlation functions
├── data_files/                      # Place your dataset here (see setup)
├── single_var_descriptives/         # Output: per-variable CSVs
└── multivariate_analysis/           # Output: multivariate CSVs
```  

---

## Setup

### Requirements

```
pandas
numpy
scipy
matplotlib
seaborn
```

Install with:

```bash
pip install -r requirements.txt
```

### Dataset

Place your CSV file in the `data_files/` folder. By default the tool expects:

```
data_files/VT Teen Study Waves 1,2,3,4 merged all youth variables.csv
```

To use a different file, update `DATA_PATH` in `config.py`.

### Missing Data Codes

Values `-99`, `-999`, and `-9999` are automatically recoded to `NaN` on load. To change this, edit `MISSING_CODES` in `config.py`.

---

## Running the App

```bash
python main_gui.py
```

---

## Usage

### Selecting Variables

Use the **Number of Variables** spinbox to set how many variable dropdowns appear. Each dropdown is searchable — start typing a variable name to filter the list.

### Buttons

| Button | Min Variables | What it does |
|---|---|---|
| **Multivariate Exploration** | 1 | Per-variable distribution plots + descriptives CSV |
| **Multivariate Visualization** | 2 | Pair grid with hue/size encoding |
| **Multivariate Correlation** | 2 | Correlation heatmap + regression pairplot |
| **Master Descriptive CSV Generator** | — | Descriptives for every column → `data_files/master_descriptives.csv` |
| **All Single Var Descriptive CSV Generator** | — | One CSV per variable → `single_var_descriptives/` |

### Plot Configuration

Hue column, size column, and color palette for plots are set in `config.py`:

```python
HUE_COL = "CGender_4"
SIZE_COL = "CAge_4"
PALETTE = "coolwarm"
```

---

## Output Files

| File | Location | Contents |
|---|---|---|
| `master_descriptives.csv` | `data_files/` | All variables × all descriptive stats |
| `<var>_descriptive.csv` | `single_var_descriptives/` | One file per variable |
| `<vars>-multivar_analysis.csv` | `multivariate_analysis/` | Descriptives for selected variable set |
