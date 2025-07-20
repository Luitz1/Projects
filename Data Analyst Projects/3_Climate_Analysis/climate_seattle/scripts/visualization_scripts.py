import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns 


def distribution_grapher(df_temp: pd.DataFrame, subplot_dims: list, figsize: list, suptitle: str):
    """

    EN:
    Plots histograms with overlaid normal distribution curves for each column in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing numerical data.
    - subplot_dims (list): A list [rows, columns] specifying the dimensions of the subplot grid.
    - figsize (list): A list [width, height] specifying the size of the entire figure.
    - suptitle (str): The main title for the entire plot.

    Returns:
    - None: Displays the plot.

    
    ES:
    Grafica histogramas con curvas de distribución normal superpuestas para cada columna en un DataFrame.

    Parámetros:
    - df (pd.DataFrame): El DataFrame de entrada que contiene datos numéricos.
    - subplot_dims (list): Una lista [filas, columnas] que especifica las dimensiones de la cuadrícula de subplots.
    - figsize (list): Una lista [ancho, alto] que especifica el tamaño de la figura completa.
    - suptitle (str): El título principal para todo el gráfico.

    Retorna:
    - None: Muestra el gráfico."""

    # Create the figure and a set of subplots
    fig, ax = plt.subplots(subplot_dims[0], subplot_dims[1], figsize=(figsize[0], figsize[1]))

    # Flatten the axes array for easy iteration if it's 2D
    ax = ax.flatten()

    # Set the main title for the entire figure
    fig.suptitle(suptitle, fontsize=14)

    # Iterate over each column in the DataFrame
    for idx, column in enumerate(df_temp.columns):

        # Fit a normal distribution to the data
        mu, sigma = stats.norm.fit(df_temp)
        # Generate x-values for the normal distribution curve
        x_hat = np.linspace(min(df_temp[column]), max(df_temp[column]), num=100)
        # Calculate the probability density function (PDF) for the normal distribution
        y_hat = stats.norm.pdf(x_hat, mu, sigma)

        # Plot the normal distribution curve
        ax[idx].plot(x_hat, y_hat,
                        linewidth=2, label="Normal Function", color="red")

        # Plot the histogram
        ax[idx].hist(x=df_temp[column],
                        density=True, bins=40, color="#3c92cf", alpha=0.6)

        # Set the title for the current subplot
        ax[idx].set_title(f'{column} Distribution', fontsize=10)
        # Set the y-axis label
        ax[idx].set_ylabel('Probability density')
        # Place the legend at the lower center
        ax[idx].legend(loc='lower center', bbox_to_anchor=(0.5, 0), ncol=1)

    # Remove y-axis labels from all subplots for cleaner presentation
    for a in ax:
        a.set_ylabel("")

    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent suptitle overlap with subplots
    plt.show()




def qq_grapher(df: pd.DataFrame, subplot_dims: list, figsize: list, suptitle: str):
    """
    EN:
    Generates Q-Q plots for each numerical column in a DataFrame to assess normality.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing numerical data.
    - subplot_dims (list): A list [rows, columns] specifying the dimensions of the subplot grid.
    - figsize (list): A list [width, height] specifying the size of the entire figure.
    - suptitle (str): The main title for the entire plot.

    Returns:
    - None: Displays the plot.

    
    ES:
    Genera gráficos Q-Q para cada columna numérica en un DataFrame para evaluar la normalidad.

    Parámetros:
    - df (pd.DataFrame): El DataFrame de entrada que contiene datos numéricos.
    - subplot_dims (list): Una lista [filas, columnas] que especifica las dimensiones de la cuadrícula de subplots.
    - figsize (list): Una lista [ancho, alto] que especifica el tamaño de la figura completa.
    - suptitle (str): El título principal para todo el gráfico.

    Retorna:
    - None: Muestra el gráfico."""

    # Create the figure and a set of subplots based on provided dimensions and figure size
    fig, ax = plt.subplots(subplot_dims[0], subplot_dims[1], figsize=(figsize[0], figsize[1]))
    # Flatten the axes array for easy iteration, especially if subplot_dims create a 2D array
    ax = ax.flatten()

    # Set the main title for the entire figure
    fig.suptitle(suptitle, fontsize=14)

    # Iterate over each column in the DataFrame
    for idx, column in enumerate(df.columns):
        # Generate the Q-Q plot for the current column
        stats.probplot(x=df[column], dist="norm", plot=ax[idx])

        # Set the title for the current subplot
        ax[idx].set_title(f'Q-Q Plot of {column}',
                          fontsize=10, fontweight="bold")

    # Remove Y and X axis labels from all subplots for a cleaner appearance
    for a in ax:
        a.set_ylabel("")  # Remove Y-axis label
        a.set_xlabel("")  # Remove X-axis label

    # Adjust the spacing between subplots to prevent overlap and improve readability
    plt.subplots_adjust(hspace=0.5, wspace=0.3)

    # Adjust the overall layout to make room for the suptitle
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # [left, bottom, right, top]
    plt.show()




def boxplots_grapher(df: pd.DataFrame, figsize: list, suptitle: str, colors: list = None):
    """
    EN:
    Generates basic boxplots for specified numerical columns in a DataFrame.
    Each boxplot is displayed in a separate subplot within a single figure.

    Parameters:
    - df (pd.DataFrame): The input pandas DataFrame containing the data.
    - figsize (list): A list [width, height] specifying the size of the entire figure.
    - suptitle (str): The main title for the entire plot.
    - colors (list, optional): A list of color strings (e.g., "#d62728", "blue") to apply
                               to each boxplot. If the list is shorter than `columns_to_plot`,
                               colors will cycle. If None, seaborn's default colors will be used.

    Returns:
    - None: Displays the plot.

    Raises:
    - ValueError: If `columns_to_plot` is empty.
    - KeyError: If any column in `columns_to_plot` is not found in the DataFrame.

    
    ES:
    Genera boxplots básicos para columnas numéricas específicas en un DataFrame.
    Cada boxplot se muestra en un subplot separado dentro de una única figura.

    Parámetros:
    - df (pd.DataFrame): El DataFrame de pandas de entrada que contiene los datos.
    - figsize (list): Una lista [ancho, alto] que especifica el tamaño de toda la figura.
    - suptitle (str): El título principal para todo el gráfico.
    - colors (list, opcional): Una lista de cadenas de color (por ejemplo, "#d62728", "blue") para aplicar
                               a cada boxplot. Si la lista es más corta que `columns_to_plot`,
                               los colores se ciclarán. Si es None, se usarán los colores predeterminados de seaborn.
    """



    # Determine the number of subplots needed
    num_plots = len(df.columns)

    # Create the figure and a set of subplots. We'll arrange them in one row.
    fig, ax = plt.subplots(1, num_plots, figsize=(figsize[0], figsize[1]))

    # Flatten the axes array for easy iteration, especially if there's only one subplot
    # In case of a single subplot, ax is not an array, so make it a list for consistent iteration
    if num_plots == 1:
        ax = [ax]
    else:
        ax = ax.flatten()

    # Set the main title for the entire figure
    fig.suptitle(suptitle, fontsize=16)

    # Iterate through each column to be plotted
    for i, var in enumerate(df):
        # Check if the column exists in the DataFrame
        if var not in df.columns:
            raise KeyError(f"Column '{var}' not found in the DataFrame.")

        # Determine the color for the current boxplot
        current_color = colors[i % len(colors)] if colors else None # Cycle colors if provided

        # Create the boxplot for the current variable
        sns.boxplot(y=df[var], ax=ax[i], color=current_color)

        # Remove the y-axis label as the main title and x-axis label might be sufficient
        ax[i].set_ylabel("")
        # Set the x-axis label to the variable name for clarity
        ax[i].set_xlabel(var)

    # Adjust the spacing between subplots to prevent overlap
    plt.subplots_adjust(wspace=0.5)
    # Adjust the layout to make room for the suptitle and prevent labels from overlapping
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # [left, bottom, right, top] coordinates normalized to figure size
    plt.show()



def corrmap_calc(df: pd.DataFrame, figsize: list=[8,8], title_graph: list = [False], 
                 cbar: bool = True, annot:bool = True, n_decimal:float = 1 ,size_font: int = 10):
    """
    The function `corrmap_calc` generates a correlation heatmap for a given DataFrame with customizable
    features such as figure size, title, color bar, annotation, and decimal precision.
    
    :param df: The `df` parameter is a pandas DataFrame that contains the data for which you want to
    calculate and visualize the correlation matrix
    :type df: pd.DataFrame
    :param figsize: The `figsize` parameter in the `corrmap_calc` function is used to specify the
    dimensions of the heatmap figure that will be created. It takes a list as input with two elements
    representing the width and height of the figure. By default, the dimensions are set to [8, 8
    :type figsize: list
    :param title_graph: The `title_graph` parameter is used to specify whether to display a title on the
    correlation heatmap graph and provide the title text and font size if it is set to `True`. It is a
    list parameter with the following elements:
    :type title_graph: list
    :param cbar: The `cbar` parameter in the `corrmap_calc` function is a boolean flag that determines
    whether to display the color bar alongside the correlation heatmap. If `cbar` is set to `True`, the
    color bar will be shown; if set to `False`, the color bar will be, defaults to True
    :type cbar: bool (optional)
    :param annot: The `annot` parameter in the `corrmap_calc` function is used to specify whether to
    display the correlation values on the heatmap. If `annot` is set to `True`, the correlation values
    will be displayed on the heatmap; if set to `False`, the values will not be displayed, defaults to
    True
    :type annot: bool (optional)
    :param n_decimal: The `n_decimal` parameter in the `corrmap_calc` function is used to specify the
    number of decimal places to display in the annotations of the correlation heatmap. This parameter
    allows you to control the precision of the correlation values shown in the heatmap. For example, if
    `n_decimal=1`,, defaults to 1
    :type n_decimal: float (optional)
    :param size_font: The `size_font` parameter in the `corrmap_calc` function is used to specify the
    font size for the annotations in the correlation heatmap. This parameter allows you to control the
    size of the text displayed on the heatmap, making it easier to read and interpret the correlation
    values between variables, defaults to 10
    :type size_font: int (optional)
    """
                 
    
    corrmat = df.select_dtypes(include=['number']).corr()
    k=10

    cm = np.corrcoef(df[corrmat].values.T)
    # Create the figure and a set of subplots
    fig, ax = plt.subplots(figsize=(figsize[0], figsize[1]))

    sns.set(font_scale=1.25)
    hm = sns.heatmap(corrmat, 
                    cbar = cbar,
                    annot = annot,
                    square = True,
                    fmt = f".{n_decimal}f",
                    annot_kws = {"size":size_font,},
                    #title = title_graph,
                    yticklabels = corrmat.columns,
                    xticklabels = corrmat.columns)
    
    if title_graph[0] == True:
        ax.set_title(title_graph[1], fontsize = title_graph[2])





def barplot_grapher(df, numerical_columns, subplot_shape:list=[2, 2], figsize=[9,6],
                    x_var:str="", y_vars=None, hue ="", title_prefix:str="", 
                    wspace=0.3, hspace=0.4, legend_title:str=""):
    """
    EN:
    Plot multiple barplots of numerical variables in a grid layout (English)

    Parameters:
    -----------
    df : pandas.DataFrame
        Data
        import matplotlib.pyplot as plt
import seaborn as snsFrame containing the data.
    numerical_columns : list of str
        List of numerical variable names to plot.
    subplot_shape : list, default [2, 2]
        Shape of the subplot grid [rows, cols].
    figsize : list, default [9, 6]
        Size of the entire figure [width, height].
    x : str, default "year"
        Column to use for the x-axis.
    y_vars : list of str, optional
        List of variables to use for y-axis (defaults to numerical_columns).
    hue : str, default "month"
        Column to use as hue for color grouping.
    title_prefix : str, default "Monthly"
        Prefix to use for subplot titles.
    wspace : float, default 0.3
        Horizontal spacing between plots.
    hspace : float, default 0.4
        Vertical spacing between plots.
    legend_title : str, default "Months"
        Title of the shared legend.

    Returns:
    --------
    None. Displays the plot.

    

    ES:

    Traza múltiples barplots de variables numéricas en una cuadrícula (Español)

    Parámetros:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos.
    numerical_columns : list of str
        Lista de nombres de variables numéricas a graficar.
    subplot_shape : list, por defecto [2, 2]
        Forma de la cuadrícula de subplots [filas, columnas].
    figsize : list, por defecto [9, 6]
        Tamaño total de la figura [ancho, alto].
    x : str, por defecto "year"
        Columna usada para el eje x.
    y_vars : list of str, opcional
        Lista de variables a usar para el eje y (por defecto igual a numerical_columns).
    hue : str, por defecto "month"
        Columna usada como hue para agrupar por color.
    title_prefix : str, por defecto "Monthly"
        Prefijo usado en los títulos de los subgráficos.
    wspace : float, por defecto 0.3
        Espacio horizontal entre gráficos.
    hspace : float, por defecto 0.4
        Espacio vertical entre gráficos.
    legend_title : str, por defecto "Months"
        Título de la leyenda compartida.

    Retorna:
    --------
    None. Muestra el gráfico.
    """
    rows, cols = subplot_shape
    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    ax = ax.flatten()

    if y_vars is None:
        y_vars = numerical_columns

    handles, labels = [], []

    for idx, var in enumerate(y_vars):
        if hue != None:
            sns.barplot(data=df, ax=ax[idx], x=x_var, y=var, hue=hue, palette="Set2")
            ax[idx].legend_.remove()
        else:
            sns.barplot(data=df, ax=ax[idx], x=x_var, y=var, palette="Set2")
        ax[idx].set_title(f"{title_prefix} {var}")

        if idx == 0:
            handles, labels = ax[idx].get_legend_handles_labels()
        

    plt.subplots_adjust(wspace=wspace, hspace=hspace)
    if hue != None:
        fig.legend(handles, labels, title=legend_title,
                    loc='center right', bbox_to_anchor=(1.05, 0.5), ncol=1)

    plt.tight_layout(rect=[0, 0, 0.95, 1])
    plt.show()

