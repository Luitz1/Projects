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