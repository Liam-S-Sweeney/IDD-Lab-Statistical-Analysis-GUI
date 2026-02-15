import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from data_loader import load_raw, load_clean
from config import HUE_COL, SIZE_COL, PALETTE

# Dataframe
raw_df = load_raw()
clean_df = load_clean()

def explore_multi_variables(*cols, palette=PALETTE):
    
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

    for col in cols:
        var_col = clean_df[col]
        non_na = var_col.dropna()
        values = non_na.to_numpy(dtype=float)
        non_na_array = np.array(non_na)

        descriptive_dict['position'].append(clean_df.columns.get_loc(col))
        descriptive_dict['variable_name'].append(col)

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
            descriptive_dict['mode'].append(stats.mode(non_na_array, axis=None, keepdims=False))

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
                descriptive_dict['skew'].append(stats.skew(np.array(list(non_na))))
                descriptive_dict['kurtosis'].append(stats.kurtosis(np.array(list(non_na))))
            
            # Measures of Frequency
            n = len(non_na_array)
            unique_values, counts = np.unique(non_na_array, return_counts = True)
    
            if len(counts.astype(int)) > (0.1*n):
                frequency = 'CONTINUOUS'
            
            else:
                frequencies_calc = counts/n * 100
                frequency_data = list(zip(unique_values, counts, frequencies_calc.astype(int)))
                freq_list = []
                for tuple in frequency_data:
                    uv, cts, freq = tuple
                    ucf = f"Unique Value: {uv}, Counts: {cts}, Frequencies: {freq}"
                    freq_list.append(ucf)
                frequency = freq_list

                    

            # Measures of Frequency | n; unique_val, count, percent
            descriptive_dict['count'].append(n)
            descriptive_dict['frequency'].append(frequency)

            # Misc
            descriptive_dict['min'].append(non_na.min())
            descriptive_dict['max'].append(non_na.max())
            descriptive_dict['se_mean'].append(non_na.std() / np.sqrt(n))
        
        # attempt to add a palette
            try:
                sns.color_palette(palette, as_cmap=True)
            except:
                pass
        
        # Shape of Distribution per Variable
            fig, (ax_probplot, ax_hist, ax_box, ax_violin, ax_swarm) = plt.subplots(1,5, figsize=(16, 6))

            # Probability Plot
            stats.probplot(
                non_na,
                dist='norm',
                plot=ax_probplot
                )
            
            points, line = ax_probplot.get_lines()

            # Style the Points
            points.set_color("steelblue")
            points.set_marker("o")
            points.set_markersize(5)
            points.set_alpha(0.7)

            # Style the fit line
            line.set_color("red")
            line.set_linewidth(2)
            line.set_linestyle("-")

            ax_probplot.set_title(f'Probability Plot')

            # Histogram
            mu, sigma = stats.norm.fit(non_na) 
            counts, bins, _ = ax_hist.hist(
                non_na,
                bins='fd',
                edgecolor='black',
                alpha=0.6,
                )
            x_dense = np.linspace(non_na.min(), non_na.max(), 500)
            pdf_dense = stats.norm.pdf(x_dense, mu, sigma)
            pdf_dense_scaled = pdf_dense * len(non_na) * (bins[1] - bins[0])

            ax_hist.plot(x_dense, pdf_dense_scaled, 'r-', lw=2,
                     label=f'Normal fit ($\\mu={mu:.2f}$, $\\sigma={sigma:.2f}$)')
            ax_hist.set_title('Histogram')
            ax_hist.legend(fontsize=7,)

            # Box Plot
            sns.boxplot(x=non_na, ax=ax_box).set(xlabel=None)
            ax_box.set_title("Box Plot")

            # Violin Plot
            sns.violinplot(x=non_na, ax=ax_violin).set(xlabel=None)
            ax_violin.set_title('Violin Plot')

            # Swarm Plot
            sns.swarmplot(x=non_na, ax=ax_swarm).set(xlabel=None)
            ax_swarm.set_title('Swarm Plot')

            plt.subplots_adjust(hspace=0.25)
            fig.suptitle(f"{col} Visualizations")
            plt.show()

    descriptive_df = pd.DataFrame(descriptive_dict)
    
    csv_title_li = [f"{i+1}.{col}" for i,col in enumerate(cols)]
    csv_title = ""

    for i_arg in csv_title_li:
        csv_title += f"{i_arg}-"
    
    try:
        descriptive_df.to_csv(rf'multivariate_analysis\{csv_title}descriptives.csv', index=False)
    except Exception as e:
        return(f"An error has occured:{e}")   
    


############

def multivariate_visualizations(*cols, hue_col=HUE_COL, size_col=SIZE_COL, palette=PALETTE):
    cols = [c for c in cols if c]
    if len(cols) < 2:
        raise ValueError("Select at least two variables.")

    # build df from selected cols
    df = pd.DataFrame({col: clean_df[col].to_numpy(float) for col in cols})

    # add hue + size columns if they exist
    if hue_col in clean_df.columns:
        df[hue_col] = clean_df[hue_col]
    else:
        hue_col = None  

    if size_col in clean_df.columns:
        df[size_col] = clean_df[size_col]
    else:
        size_col = None
    
    # attempt to add a palette
    try:
        sns.color_palette(palette, as_cmap=True)
    except:
        pass

    g = sns.PairGrid(data=df, diag_sharey=False, hue=hue_col)

    g.map_diag(sns.histplot)
    g.map_lower(sns.scatterplot, size=df[size_col] if size_col else None)
    g.map_upper(sns.kdeplot)

    if hue_col:
        g.add_legend(title=hue_col)

    plt.show()

#########

def correlational_analysis(*cols, hue_col="CGender_4", palette=PALETTE):
    # clean selected columns
    cols = [c for c in cols if c]

    if len(cols) < 2:
        raise ValueError("Select at least two variables for correlation analysis.")

    # build df from selected cols that actually exist
    missing = [c for c in cols if c not in clean_df.columns]
    if missing:
        raise KeyError(f"Missing columns in dataset: {missing}")

    df = clean_df[cols].copy()

    # attempt to add a palette
    try:
        sns.color_palette(palette, as_cmap=True)
    except:
        pass

    # ---- Heatmap (correlation matrix) ----
    corr = df.corr(numeric_only=True)

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        square=True
    )

    # ---- Pairplot ----
    hue_to_use = None
    if hue_col and hue_col in clean_df.columns:
        df[hue_col] = clean_df[hue_col]
        hue_to_use = hue_col

    sns.pairplot(
        data=df,
        hue=hue_to_use,     
        kind="reg"
    )

    plt.show()
     