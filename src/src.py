import pylab as plt

import pandas as pd

import seaborn as sns

#Devuelve la gráfica de columnas x null/nan
def getGraphic(dataframe):
    
    plt.figure(figsize=(10, 6))

    return sns.heatmap(dataframe.isnull(), yticklabels=False, cmap='viridis', cbar=False)

#Devuelve un diccionario con los valores de la columna ordenados por frecuencia
def getDic(dataframe, column):

    return dict(dataframe[column].value_counts())

#Cambia valor string por otro más genérico
def setChange(dataframe, column, lst):
    
    dataframe[column] = dataframe[column].str.lower()

    for i in lst:

        dataframe[column][dataframe[column].str.contains(i)] = i.upper()