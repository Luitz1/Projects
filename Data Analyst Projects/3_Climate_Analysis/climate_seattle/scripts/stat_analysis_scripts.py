import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")






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










def anova_test(df, numeric_var, categorical_var):
    """
    EN:
    Perform complete ANOVA analysis with explanatory visualizations.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with data
    numeric_var : str
        Numeric variable name (dependent)
    categorical_var : str
        Categorical variable name (independent)
    
    Returns:
    --------
    dict
        Dictionary with ANOVA results

        
    ES:
    Realiza análisis ANOVA completo con visualizaciones explicativas.
    
    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos
    numeric_var : str
        Nombre de variable numérica (dependiente)
    categorical_var : str
        Nombre de variable categórica (independiente)
    
    Retorna:
    --------
    dict
        Diccionario con resultados del ANOVA

    """
    
    print("="*60)
    print(f"ANÁLISIS ANOVA: {numeric_var} vs {categorical_var}")
    print("="*60)
    
    # Prepare data groups
    groups = []
    categories = df[categorical_var].unique()
    
    for category in categories:
        group = df[df[categorical_var] == category][numeric_var]
        groups.append(group)
    
    # Descriptive statistics by group
    print("\n📊 ESTADÍSTICAS DESCRIPTIVAS POR GRUPO:")
    print("-" * 50)
    
    descriptive_stats = df.groupby(categorical_var)[numeric_var].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(4)
    
    print(descriptive_stats)
    
    # Perform ANOVA
    print(f"\n🔍 PRUEBA ANOVA DE UNA VÍA:")
    print("-" * 50)
    
    f_stat, p_val = stats.f_oneway(*groups)
    
    print(f"Estadístico F: {f_stat:.4f}")
    print(f"p-value: {p_val:.4f}")
    
    # Interpretation
    alpha = 0.05
    print(f"\nInterpretación (α = {alpha}):")
    if p_val < alpha:
        print("✅ RECHAZAMOS H₀: Hay diferencias significativas entre grupos")
        print("   Las medias de los grupos son estadísticamente diferentes")
    else:
        print("❌ NO RECHAZAMOS H₀: No hay diferencias significativas entre grupos")
        print("   Las medias de los grupos son estadísticamente similares")
    
    # Check assumptions
    print(f"\n🔧 VERIFICACIÓN DE SUPUESTOS:")
    print("-" * 50)
    
    # Normality test for each group
    print("1. Normalidad por grupo:")
    for i, category in enumerate(categories):
        group = groups[i]
        if len(group) < 5000:  # Shapiro-Wilk limitations with large samples
            _, p_norm = stats.shapiro(group)
            print(f"   {category}: p = {p_norm:.4f} {'✅' if p_norm > 0.05 else '❌'}")
    
    # Homoscedasticity test
    _, p_levene = stats.levene(*groups)
    print(f"2. Homocedasticidad (Levene): p = {p_levene:.4f} {'✅' if p_levene > 0.05 else '❌'}")
    
    # Effect size calculation (Eta squared)
    grand_mean = df[numeric_var].mean()
    ss_between = sum([len(group) * (group.mean() - grand_mean)**2 for group in groups])
    ss_total = sum([(x - grand_mean)**2 for x in df[numeric_var]])
    eta_squared = ss_between / ss_total
    
    print(f"\n📏 TAMAÑO DEL EFECTO:")
    print("-" * 50)
    print(f"Eta² = {eta_squared:.4f}")
    
    if eta_squared < 0.01:
        effect_size = "Muy pequeño"
    elif eta_squared < 0.06:
        effect_size = "Pequeño"
    elif eta_squared < 0.14:
        effect_size = "Moderado"
    else:
        effect_size = "Grande"
    
    print(f"Interpretación: {effect_size}")
    
    # Create visualizations
    create_anova_plots(df, numeric_var, categorical_var)
    
    # Return results
    return {
        'f_statistic': f_stat,
        'p_value': p_val,
        'eta_squared': eta_squared,
        'group_stats': descriptive_stats,
        'significant': p_val < alpha
    }

def create_anova_plots(df, num_var, cat_var):
    """
    EN:

    Create explanatory visualizations for ANOVA analysis.

    ES:
    
    Crea visualizaciones explicativas para el análisis ANOVA.

    """
    
    # Set up subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'Análisis ANOVA: {num_var} vs {cat_var}', fontsize=16, fontweight='bold')
    
    # Box plot
    sns.boxplot(data=df, x=cat_var, y=num_var, ax=axes[0,0])
    axes[0,0].set_title('Box Plot - Distribución por Grupo')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # Violin plot
    sns.violinplot(data=df, x=cat_var, y=num_var, ax=axes[0,1])
    axes[0,1].set_title('Violin Plot - Densidad por Grupo')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Overlapping histograms
    for category in df[cat_var].unique():
        data = df[df[cat_var] == category][num_var]
        axes[1,0].hist(data, alpha=0.7, label=category, bins=20)
    
    axes[1,0].set_title('Histogramas Superpuestos')
    axes[1,0].set_xlabel(num_var)
    axes[1,0].set_ylabel('Frecuencia')
    axes[1,0].legend()
    
    # Means with confidence intervals
    means = df.groupby(cat_var)[num_var].mean()
    errors = df.groupby(cat_var)[num_var].sem() * 1.96  # 95% CI
    
    x_pos = range(len(means))
    axes[1,1].bar(x_pos, means, yerr=errors, capsize=5, alpha=0.7)
    axes[1,1].set_title('Medias con Intervalos de Confianza 95%')
    axes[1,1].set_xlabel(cat_var)
    axes[1,1].set_ylabel(f'Media de {num_var}')
    axes[1,1].set_xticks(x_pos)
    axes[1,1].set_xticklabels(means.index, rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    plt.show()

def posthoc_test(df, numeric_var, categorical_var):
    """
    EN:
    Perform post-hoc analysis (Tukey HSD) if ANOVA is significant.

    ES:
    Realiza análisis post-hoc (Tukey HSD) si el ANOVA es significativo.
    """
    from scipy.stats import tukey_hsd
    
    print("\n🔍 ANÁLISIS POST-HOC (Tukey HSD):")
    print("-" * 50)
    
    # Prepare data for Tukey HSD
    groups = []
    categories = df[categorical_var].unique()
    
    for category in categories:
        group = df[df[categorical_var] == category][numeric_var]
        groups.append(group)
    
    # Perform Tukey HSD
    try:
        tukey_result = tukey_hsd(*groups)
        
        print("Comparaciones pareadas:")
        print(f"{'Grupo 1':<15} {'Grupo 2':<15} {'Diferencia':<12} {'p-value':<10} {'Significativo'}")
        print("-" * 70)
        
        for i in range(len(categories)):
            for j in range(i+1, len(categories)):
                p_val = tukey_result.pvalue[i, j]
                diff = abs(groups[i].mean() - groups[j].mean())
                sig = "✅" if p_val < 0.05 else "❌"
                
                print(f"{categories[i]:<15} {categories[j]:<15} {diff:<12.4f} {p_val:<10.4f} {sig}")
    
    except Exception as e:
        print(f"Error en análisis post-hoc: {e}")
        print("Usar otros métodos como Bonferroni o t-tests pareados")