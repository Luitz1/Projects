import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def descriptive_statistics(df):
    """
    EN:
    Calculates full descriptive statistics for a DataFrame with numeric columns.

    Parameters:
    -----------
    df: pandas.DataFrame
        DataFrame with numeric columns

    Returns:
    --------
    pandas.DataFrame
        DataFrame with all descriptive statistics per column


    ES:
    Calcula estadísticos descriptivos completos para un DataFrame con columnas numéricas.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame con columnas numéricas
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame con todos los estadísticos descriptivos por columna
    """
    
    # Verificar que el DataFrame no esté vacío
    if df.empty:
        raise ValueError("El DataFrame está vacío")
    
    # Seleccionar solo columnas numéricas
    df_numeric = df.select_dtypes(include=[np.number])
    
    if df_numeric.empty:
        raise ValueError("No se encontraron columnas numéricas en el DataFrame")
    
    # Diccionario para almacenar los resultados
    estadisticos = {}
    
    for columna in df_numeric.columns:
        serie = df_numeric[columna].dropna()  # Eliminar valores NaN para cálculos
        
        # Estadísticos básicos
        estadisticos[columna] = {
            # Medidas de tendencia central
            'media': serie.mean(),
            'mediana': serie.median(),
            'moda': serie.mode().iloc[0] if not serie.mode().empty else np.nan,
            
            # Medidas de dispersión
            'desviacion_estandar': serie.std(),
            'varianza': serie.var(),
            'rango': serie.max() - serie.min(),
            'rango_intercuartil': serie.quantile(0.75) - serie.quantile(0.25),
            
            # Valores extremos
            'minimo': serie.min(),
            'maximo': serie.max(),
            
            # Cuartiles y percentiles
            'q1': serie.quantile(0.25),
            'q3': serie.quantile(0.75),
            'percentil_10': serie.quantile(0.10),
            'percentil_90': serie.quantile(0.90),
            
            # Medidas de forma
            'asimetria': serie.skew(),
            'curtosis': serie.kurtosis(),
            
            # Información adicional
            'count': len(serie),
            'valores_nulos': df_numeric[columna].isnull().sum(),
            'valores_unicos': serie.nunique(),
            
            # Coeficiente de variación
            'coef_variacion': (serie.std() / serie.mean()) * 100 if serie.mean() != 0 else np.nan,
            
            # Error estándar de la media
            'error_estandar': serie.std() / np.sqrt(len(serie)) if len(serie) > 0 else np.nan,
            
            # Intervalo de confianza 95% para la media
            'ic_inferior_95': serie.mean() - 1.96 * (serie.std() / np.sqrt(len(serie))) if len(serie) > 0 else np.nan,
            'ic_superior_95': serie.mean() + 1.96 * (serie.std() / np.sqrt(len(serie))) if len(serie) > 0 else np.nan,
        }
    
    # Convertir a DataFrame para mejor visualización
    resultado = pd.DataFrame(estadisticos).T
    
    # Redondear los valores para mejor legibilidad
    resultado = resultado.round(4)
    
    return resultado

def summary_statistics(df):
    """
    EN:
    Helper function that provides a more compact summary of the key statistics.

    Parameters:
    -----------
    df: pandas.DataFrame
        DataFrame with numeric columns

    Returns:
    --------
    pandas.DataFrame
        DataFrame with key statistics


    ES:
    Función auxiliar que proporciona un resumen más compacto de los estadísticos principales.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame con columnas numéricas
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame con estadísticos principales

    """
    
    estadisticos_completos = descriptive_statistics(df)
    
    # Seleccionar solo los estadísticos más importantes
    columnas_principales = [
        'count', 'media', 'mediana', 'moda', 'desviacion_estandar', 
        'minimo', 'q1', 'q3', 'maximo', 'asimetria', 'curtosis'
    ]
    
    return estadisticos_completos[columnas_principales]

def interpret_statistics(df):
    """
    EN:
    Function that provides a basic interpretation of statistics.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with numeric columns

    Returns:
    --------
    dict
        Dictionary with interpretations per column

    
    ES:
    Función que proporciona una interpretación básica de los estadísticos.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame con columnas numéricas
    
    Returns:
    --------
    dict
        Diccionario con interpretaciones por columna
    """
    
    stats_df = descriptive_statistics(df)
    interpretaciones = {}
    
    for columna in stats_df.index:
        interpretacion = []
        
        # Interpretación de asimetría
        asimetria = stats_df.loc[columna, 'asimetria']
        if abs(asimetria) < 0.5:
            interpretacion.append("Distribución aproximadamente simétrica")
        elif asimetria > 0.5:
            interpretacion.append("Distribución con sesgo hacia la derecha")
        else:
            interpretacion.append("Distribución con sesgo hacia la izquierda")
        
        # Interpretación de curtosis
        curtosis = stats_df.loc[columna, 'curtosis']
        if curtosis > 0:
            interpretacion.append("Distribución leptocúrtica (más puntiaguda)")
        elif curtosis < 0:
            interpretacion.append("Distribución platícúrtica (más plana)")
        else:
            interpretacion.append("Distribución mesocúrtica (curtosis normal)")
        
        # Coeficiente de variación
        coef_var = stats_df.loc[columna, 'coef_variacion']
        if coef_var < 15:
            interpretacion.append("Baja variabilidad")
        elif coef_var < 35:
            interpretacion.append("Variabilidad moderada")
        else:
            interpretacion.append("Alta variabilidad")
        
        interpretaciones[columna] = "; ".join(interpretacion)
    
    return interpretaciones