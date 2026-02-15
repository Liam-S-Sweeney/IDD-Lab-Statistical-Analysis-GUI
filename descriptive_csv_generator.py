import pandas as pd
import numpy as np
import scipy.stats as stats
from data_loader import load_raw, load_clean

# Dataframe
raw_df = load_raw()
clean_df = load_clean()

# Datatype Classification Function
def classify_variable(values: np.ndarray):
    uniq = np.unique(values)
    n_unique = uniq.size

    if n_unique <= 20:
        return "discrete"
    else:
        return "continuous"


def master_descriptive_csv_generator():  
    descriptive_dict = {
        # Variable Info
        'position': [],
        'variable_name': [],

        # Measures of Central Tendency
        'mean': [],
        'median': [],
        'mode': [],

        # Measures of Variability
        'var': [],
        'std': [],
        'range': [],
        'q1': [],
        'q3': [],
        'iqr': [],

        # Measures of Shape
        'skew': [],
        'kurtosis': [],

        # Measures of Frequency
        'count': [],
        'frequency': [],

        # Misc
        'min': [],
        'max': [],
        'se_mean': [],
    }


    all_var_names = [var for var in clean_df.columns]

    for arg in all_var_names:
        var_col = clean_df[arg]
        non_na = var_col.dropna()
        values = non_na.to_numpy(dtype=float)
        non_na_array = np.array(non_na)

        descriptive_dict['position'].append(clean_df.columns.get_loc(arg))
        descriptive_dict['variable_name'].append(arg)

        if non_na.empty:
            descriptive_dict['mean'].append(np.nan)
            descriptive_dict['median'].append(np.nan)
            descriptive_dict['mode'].append(np.nan)

            descriptive_dict['var'].append(np.nan)
            descriptive_dict['std'].append(np.nan)
            descriptive_dict['range'].append(np.nan)
            descriptive_dict['q1'].append(np.nan)
            descriptive_dict['q3'].append(np.nan)
            descriptive_dict['iqr'].append(np.nan)

            descriptive_dict['skew'].append(np.nan)
            descriptive_dict['kurtosis'].append(np.nan)

            descriptive_dict['count'].append(np.nan)
            descriptive_dict['frequency'].append(np.nan)

            descriptive_dict['min'].append(np.nan)
            descriptive_dict['max'].append(np.nan)
            descriptive_dict['se_mean'].append(np.nan)
        
        # Descriptive Computations
        else:
            # Measures of Central Tendency
            descriptive_dict['mean'].append(non_na.mean())
            descriptive_dict['median'].append(non_na.median())
            descriptive_dict['mode'].append(stats.mode(non_na_array, axis=None, keepdims=False).mode)

            # Measures of Variability
            descriptive_dict['var'].append(non_na.var())
            descriptive_dict['std'].append(non_na.std())
            descriptive_dict['range'].append(non_na.max()-non_na.min())
            descriptive_dict['q1'].append(np.percentile(non_na, 25))
            descriptive_dict['q3'].append(np.percentile(non_na, 75))
            descriptive_dict['iqr'].append(np.percentile(non_na, 75)-np.percentile(non_na, 25))

            # Measures of Shape
            if values.size < 3 or np.isclose(values.std(ddof=0), 0.0, atol=1e-8):
                descriptive_dict['skew'].append(np.nan)
                descriptive_dict['kurtosis'].append(np.nan)    
            else:
                descriptive_dict['skew'].append(stats.skew(values))
                descriptive_dict['kurtosis'].append(stats.kurtosis(np.array(list(non_na))))
            
            # Measures of Frequency
            n = non_na_array.size
            unique_values, counts = np.unique(non_na_array, return_counts=True)

            n_unique = len(counts)

            if n_unique > 20:
                frequency = "CONTINUOUS"
            else:
                percents = np.round((counts / n) * 100, 2)
                frequency = [(float(uv), int(ct), float(p)) for uv, ct, p in zip(unique_values, counts, percents)] 

            # Measures of Frequency | n; unique_val, count, percent
            descriptive_dict['count'].append(n)
            descriptive_dict['frequency'].append(frequency)

            # Misc
            descriptive_dict['min'].append(non_na.min())
            descriptive_dict['max'].append(non_na.max())
            descriptive_dict['se_mean'].append(non_na.std() / np.sqrt(n))
        


    descriptive_df = pd.DataFrame(descriptive_dict)
    
    descriptive_df.to_csv('data_files\master_descriptives.csv', index=False)



def all_single_var_descriptive_csv_generator():

    all_var_names = [var for var in clean_df.columns]

    for arg in all_var_names:

        descriptive_dict = {
        # Variable Info
        'position': [],
        'variable_name': [],

        # Measures of Central Tendency
        'mean': [],
        'median': [],
        'mode': [],

        # Measures of Variability
        'var': [],
        'std': [],
        'range': [],
        'q1': [],
        'q3': [],
        'iqr': [],

        # Measures of Shape
        'skew': [],
        'kurtosis': [],

        # Measures of Frequency
        'count': [],
        'frequency': [],

        # Misc
        'min': [],
        'max': [],
        'se_mean': [],
        }

        var_col = clean_df[arg]
        non_na = var_col.dropna()
        values = non_na.to_numpy(dtype=float)
        non_na_array = np.array(non_na)

        descriptive_dict['position'].append(clean_df.columns.get_loc(arg))
        descriptive_dict['variable_name'].append(arg)

        if non_na.empty:
            descriptive_dict['mean'].append(np.nan)
            descriptive_dict['median'].append(np.nan)
            descriptive_dict['mode'].append(np.nan)

            descriptive_dict['var'].append(np.nan)
            descriptive_dict['std'].append(np.nan)
            descriptive_dict['range'].append(np.nan)
            descriptive_dict['q1'].append(np.nan)
            descriptive_dict['q3'].append(np.nan)
            descriptive_dict['iqr'].append(np.nan)

            descriptive_dict['skew'].append(np.nan)
            descriptive_dict['kurtosis'].append(np.nan)

            descriptive_dict['count'].append(np.nan)
            descriptive_dict['frequency'].append(np.nan)

            descriptive_dict['min'].append(np.nan)
            descriptive_dict['max'].append(np.nan)
            descriptive_dict['se_mean'].append(np.nan)
        
        # Descriptive Computations
        else:
            # Measures of Central Tendency
            descriptive_dict['mean'].append(non_na.mean())
            descriptive_dict['median'].append(non_na.median())
            descriptive_dict['mode'].append(stats.mode(non_na_array, axis=None, keepdims=False).mode)

            # Measures of Variability
            descriptive_dict['var'].append(non_na.var())
            descriptive_dict['std'].append(non_na.std())
            descriptive_dict['range'].append(non_na.max()-non_na.min())
            descriptive_dict['q1'].append(np.percentile(non_na, 25))
            descriptive_dict['q3'].append(np.percentile(non_na, 75))
            descriptive_dict['iqr'].append(np.percentile(non_na, 75)-np.percentile(non_na, 25))

            # Measures of Shape
            if values.size < 3 or np.isclose(values.std(ddof=0), 0.0, atol=1e-8):
                descriptive_dict['skew'].append(np.nan)
                descriptive_dict['kurtosis'].append(np.nan)    
            else:
                descriptive_dict['skew'].append(stats.skew(values))
                descriptive_dict['kurtosis'].append(stats.kurtosis(np.array(list(non_na))))
            
            # Measures of Frequency
            n = non_na_array.size
            unique_values, counts = np.unique(non_na_array, return_counts=True)

            n_unique = len(counts)

            if n_unique > 20:
                frequency = "CONTINUOUS"
            else:
                percents = np.round((counts / n) * 100, 2)
                frequency = [(float(uv), int(ct), float(p)) for uv, ct, p in zip(unique_values, counts, percents)] 

            # Measures of Frequency | n; unique_val, count, percent
            descriptive_dict['count'].append(n)
            descriptive_dict['frequency'].append(frequency)

            # Misc
            descriptive_dict['min'].append(non_na.min())
            descriptive_dict['max'].append(non_na.max())
            descriptive_dict['se_mean'].append(non_na.std() / np.sqrt(n))
        


            descriptive_df = pd.DataFrame(descriptive_dict)
    
            descriptive_df.to_csv(rf'single_var_descriptives\{arg}_descriptive.csv', index=False)

            

