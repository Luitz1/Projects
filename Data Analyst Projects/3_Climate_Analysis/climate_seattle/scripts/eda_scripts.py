import numpy as np
import pandas as pd

def unique_values(df_no_num):
    """
    EN:
    Analyzes a pandas DataFrame to extract unique values and their counts for each column.
    The function iterates through each column of the input DataFrame, calculates the frequency
    of each unique value, and stores this information. It returns a list of lists of dictionaries,
    where each inner list corresponds to a column from the original DataFrame, and each dictionary
    within that list represents a unique value and its count for that column.

    Parameters:
    - df_no_num (pd.DataFrame): The input DataFrame from which to extract unique values and counts.
                                It's typically expected to contain non-numerical (categorical or object)
                                data, but will work with any column type.

    Returns:
    - list[list[dict]]: A list where each element is another list of dictionaries.
                        Each inner list corresponds to a column in the input DataFrame.
                        Each dictionary in the inner list contains two key-value pairs:
                        - A key dynamically named 'Un_Value {column_name}' holding the unique value.
                        - A key 'Count' holding the frequency of that unique value.



    ES:
    Analiza un DataFrame de pandas para extraer los valores únicos y sus recuentos para cada columna.
    La función itera a través de cada columna del DataFrame de entrada, calcula la frecuencia de cada
    valor único y almacena esta información. Devuelve una lista de listas de diccionarios, donde cada
    lista interna corresponde a una columna del DataFrame original, y cada diccionario dentro de esa
    lista representa un valor único y su recuento para esa columna.

    Parámetros:
    - df_no_num (pd.DataFrame): El DataFrame de entrada del cual extraer los valores únicos y sus recuentos.
                                Se espera típicamente que contenga datos no numéricos (categóricos u objetos),
                                pero funcionará con cualquier tipo de columna.

    Retorna:
    - list[list[dict]]: Una lista donde cada elemento es otra lista de diccionarios.
                        Cada lista interna corresponde a una columna en el DataFrame de entrada.
                        Cada diccionario en la lista interna contiene dos pares clave-valor:
                        - Una clave nombrada dinámicamente 'Un_Value {nombre_columna}' que contiene el valor único.
                        - Una clave 'Count' que contiene la frecuencia de ese valor único.

    """
    # Initialize List
    df_list = []
    for idx, column in enumerate(df_no_num):
            # Initialize List
            newdf = []
            # Cycle that runs through the intems and counts
            for unique_val, count in df_no_num[column].value_counts().items():
                # Add Headers
                newdf.append({
                        f'Un_Value {column}': unique_val,
                        'Count': count
                        })
            # List to add the dictionaries of the columns traversed
            df_list.append(newdf)
    return df_list