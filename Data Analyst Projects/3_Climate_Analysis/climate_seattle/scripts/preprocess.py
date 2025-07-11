import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def identify_outliers(df, column, method='iqr', factor=1.5, z_threshold=3, show_plot=True):
    """
    EN:

    Identifies outliers in a DataFrame column.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column : str
        Name of the column to analyze.
    method : str, default 'iqr'
        Outlier detection method: 'iqr', 'zscore', or 'both'.
    factor : float, default 1.5
        Multiplier for IQR method.
    z_threshold : float, default 3
        Threshold for Z-score method.
    show_plot : bool, default True
        Whether to show summary plots.

    Returns:
    --------
    dict with outlier information and boolean masks for each method.

    ES:
    Identifica outliers en una columna de un DataFrame.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene los datos.
    column : str
        Nombre de la columna a analizar.
    method : str, por defecto 'iqr'
        Método de detección de outliers: 'iqr', 'zscore' o 'both'.
    factor : float, por defecto 1.5
        Factor multiplicador para el método IQR.
    z_threshold : float, por defecto 3
        Umbral para el método Z-score.
    show_plot : bool, por defecto True
        Indica si se deben mostrar gráficos resumen.

    Retorna:
    --------
    dict con información de outliers y máscaras booleanas para cada método.


    """

    
    # Verificaciones básicas
    if column not in df.columns:
        raise ValueError(f"La columna '{column}' no existe en el DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"La columna '{column}' no es numérica")
    
    data = df[column].dropna()
    results = {}
    
    # Método IQR
    if method in ['iqr', 'both']:
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR
        
        iqr_outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        
        results['iqr'] = {
            'mask': iqr_outliers,
            'count': iqr_outliers.sum(),
            'percentage': (iqr_outliers.sum() / len(df)) * 100,
            'bounds': (lower_bound, upper_bound),
            'outlier_values': df[iqr_outliers][column].tolist()
        }
    
    # Método Z-Score
    if method in ['zscore', 'both']:
        z_scores = np.abs(stats.zscore(data))
        zscore_mask = pd.Series(False, index=df.index)
        zscore_mask[data.index[z_scores > z_threshold]] = True
        
        results['zscore'] = {
            'mask': zscore_mask,
            'count': zscore_mask.sum(),
            'percentage': (zscore_mask.sum() / len(df)) * 100,
            'threshold': z_threshold,
            'outlier_values': df[zscore_mask][column].tolist()
        }
    
    # Mostrar resumen
    print(f"=== ANÁLISIS DE OUTLIERS: {column} ===")
    print(f"Total de datos: {len(df)}")
    print(f"Valores nulos: {df[column].isnull().sum()}")
    print(f"Estadísticas básicas:")
    print(f"  Media: {data.mean():.2f}")
    print(f"  Mediana: {data.median():.2f}")
    print(f"  Desv. estándar: {data.std():.2f}")
    print()
    
    for method_name, result in results.items():
        print(f"Método {method_name.upper()}:")
        print(f"  Outliers encontrados: {result['count']}")
        print(f"  Porcentaje: {result['percentage']:.2f}%")
        if method_name == 'iqr':
            print(f"  Límites: ({result['bounds'][0]:.2f}, {result['bounds'][1]:.2f})")
        print()
    
    # Visualizaciones
    if show_plot:
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        # Histograma
        axes[0].hist(data, bins=30, alpha=0.7, edgecolor='black')
        axes[0].set_title(f'Histograma: {column}')
        axes[0].set_xlabel(column)
        axes[0].set_ylabel('Frecuencia')
        
        # Boxplot
        axes[1].boxplot(data)
        axes[1].set_title(f'Boxplot: {column}')
        axes[1].set_ylabel(column)
        
        # Scatter plot con outliers resaltados
        axes[2].scatter(range(len(df)), df[column], alpha=0.6, label='Normal')
        
        if method in ['iqr', 'both']:
            outlier_indices = df[results['iqr']['mask']].index
            axes[2].scatter(outlier_indices, df.loc[outlier_indices, column], 
                          color='blue', alpha=0.8, label='Outliers IQR')
        
        axes[2].set_title(f'Scatter Plot: {column}')
        axes[2].set_xlabel('Índice')
        axes[2].set_ylabel(column)
        axes[2].legend()
        
        plt.tight_layout()
        plt.show()
    
    return results

def treat_outliers(df, column, outlier_mask, method='cap', custom_value=None, inplace=False):

    """
    EN:
    
    Handles outliers in a DataFrame column.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column : str
        Name of the column to process.
    outlier_mask : pandas.Series
        Boolean mask indicating outlier positions.
    method : str, default 'cap'
        Treatment method: 'remove', 'cap', 'median', 'mean', 'custom'.
    custom_value : float, optional
        Custom value to replace outliers (only used when method='custom').
    inplace : bool, default False
        Whether to modify the original DataFrame.

    Returns:
    --------
    pandas.DataFrame with treated outliers.

    
    ES:

    Trata outliers en una columna de un DataFrame.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene los datos.
    column : str
        Nombre de la columna a tratar.
    outlier_mask : pandas.Series
        Máscara booleana que indica la posición de los outliers.
    method : str, por defecto 'cap'
        Método de tratamiento: 'remove', 'cap', 'median', 'mean', 'custom'.
    custom_value : float, opcional
        Valor personalizado para reemplazar outliers (solo cuando method='custom').
    inplace : bool, por defecto False
        Indica si se debe modificar el DataFrame original.

    Retorna:
    --------
    pandas.DataFrame con los outliers tratados.



    """

    
    if not inplace:
        df = df.copy()
    
    outliers_count = outlier_mask.sum()
    
    if outliers_count == 0:
        print("No hay outliers para tratar")
        return df
    
    print(f"=== TRATAMIENTO DE OUTLIERS: {column} ===")
    print(f"Outliers a tratar: {outliers_count}")
    
    if method == 'remove':
        # Eliminar filas con outliers
        df = df[~outlier_mask]
        print(f"Filas eliminadas: {outliers_count}")
        
    elif method == 'cap':
        # Limitar a percentiles 5 y 95
        p5 = df[column].quantile(0.05)
        p95 = df[column].quantile(0.95)
        df.loc[outlier_mask, column] = df.loc[outlier_mask, column].clip(p5, p95)
        print(f"Valores limitados entre {p5:.2f} y {p95:.2f}")
        
    elif method == 'median':
        # Reemplazar con la mediana
        median_val = df[column].median()
        df.loc[outlier_mask, column] = median_val
        print(f"Outliers reemplazados con mediana: {median_val:.2f}")
        
    elif method == 'mean':
        # Reemplazar con la media (sin outliers)
        mean_val = df[~outlier_mask][column].mean()
        df.loc[outlier_mask, column] = mean_val
        print(f"Outliers reemplazados con media: {mean_val:.2f}")
        
    elif method == 'custom':
        # Reemplazar con valor personalizado
        if custom_value is None:
            raise ValueError("Debe proporcionar un valor personalizado")
        df.loc[outlier_mask, column] = custom_value
        print(f"Outliers reemplazados con valor personalizado: {custom_value}")
        
    else:
        raise ValueError("Método no válido. Use: 'remove', 'cap', 'median', 'mean', 'custom'")
    
    # Mostrar estadísticas después del tratamiento
    print(f"\nEstadísticas después del tratamiento:")
    print(f"  Media: {df[column].mean():.2f}")
    print(f"  Mediana: {df[column].median():.2f}")
    print(f"  Desv. estándar: {df[column].std():.2f}")
    print(f"  Filas restantes: {len(df)}")
    
    return df

def quick_outlier_analysis(df, column, method='iqr', treatment='cap', show_comparison=True):

    """
    EN:

    Quick full outlier analysis function.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data.
    column : str
        Name of the column to analyze.
    method : str, default 'iqr'
        Outlier detection method: 'iqr' or 'zscore'.
    treatment : str, default 'cap'
        Outlier treatment method: 'remove', 'cap', 'median', or 'mean'.
    show_comparison : bool, default True
        Whether to display before/after histograms.

    Returns:
    --------
    pandas.DataFrame with outliers treated.

    ES:

    Función rápida para análisis completo de outliers.

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame que contiene los datos.
    column : str
        Nombre de la columna a analizar.
    method : str, por defecto 'iqr'
        Método de detección de outliers: 'iqr' o 'zscore'.
    treatment : str, por defecto 'cap'
        Método de tratamiento: 'remove', 'cap', 'median' o 'mean'.
    show_comparison : bool, por defecto True
        Indica si se deben mostrar histogramas antes y después.

    Retorna:
    --------
    pandas.DataFrame con outliers tratados.

    
    """


    # Identificar outliers
    outlier_results = identify_outliers(df, column, method=method)
    
    # Usar la máscara del método seleccionado
    mask = outlier_results[method]['mask']
    
    # Tratar outliers
    df_treated = treat_outliers(df, column, mask, method=treatment)
    
    # Comparación visual
    if show_comparison and len(df_treated) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Antes
        axes[0].hist(df[column].dropna(), bins=30, alpha=0.7, color='blue', edgecolor='black')
        axes[0].set_title(f'Antes del tratamiento\n{column}')
        axes[0].set_xlabel(column)
        axes[0].set_ylabel('Frecuencia')
        
        # Después  
        axes[1].hist(df_treated[column].dropna(), bins=30, alpha=0.7, color='orange', edgecolor='black')
        axes[1].set_title(f'Después del tratamiento\n{column}')
        axes[1].set_xlabel(column)
        axes[1].set_ylabel('Frecuencia')
        
        plt.tight_layout()
        plt.show()
    
    return df_treated