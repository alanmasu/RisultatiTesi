#tool per farei i grafici
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def seabornConfig():
    # Set the style
    sns.set_style("whitegrid")


def createChart(filename, img_filename):
    plt.clf()
    
    # Leggi il dataframe dal file CSV
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading dataframe from file {filename}: {e}")
        return 0
    
    if df.empty:
        print(f"Dataframe is empty")
        return 0
    
    # Printo il dataframe
    print(df)

    # Preprocessing del dataframe
    # Cerca i valori NaN nella colonna 'timestamp(us)' e calcolali come timestamp(ticks)/40
    if 'timestamp(us)' in df.columns:
        df['timestamp(us)'] = df['timestamp(us)'].fillna(df['timestamp(tiks)'] / 40)
    else:
        print("Column 'timestamp(us)' not found in dataframe. Skipping NaN replacement.")
    

    print("\nDataframe after preprocessing:")
    print(df)
    
    sizes = df['size(bit)'].unique()
    
    for size in sizes:
        print (f"\nSize: {a} bits")
        df_FPGA = df[(df['platform'] == 'FPGA') & (df['size(bit)'] == size)]
        df_RP   = df[(df['platform'] == 'RP2350') & (df['size(bit)'] == size)]
        


    

if __name__ == "__main__":
    # Set the style
    seabornConfig()
    

    # Create the chart
    createChart("DatiRow/RisultatiRow.csv", "Immagini/risultati.png")