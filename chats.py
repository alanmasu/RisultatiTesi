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
    
    df['BTPU'] = df['Caricamento'] + df['Settaggio'] + df['Inizializzazione'] + df['ComputazioneBTPU'] + df['LetturaRisultato']
    
    # print(df[['BTPU', 'ComputazioneSerialeFast']])
    
    df_FPGA = df[df['platform'] == 'FPGA']
    df_RP2350 = df[df['platform'] == 'RP2350']
    
    df_RP2350['ComputazioneBTPU'] = df_FPGA['ComputazioneBTPU']
    
    sns.lineplot(x='size(bit)', y='ComputazioneSerialeFast', data=df_FPGA, label='RISC-V', color='blue')
    sns.lineplot(x='size(bit)', y='ComputazioneSerialeFast', data=df_RP2350, label='RP2350', color='orange')
    sns.lineplot(x='size(bit)', y='BTPU', data=df_FPGA, label='BTPU', color='red')
    sns.lineplot(x='size(bit)', y='BTPU', data=df_RP2350, label='BTPU (*sim)', color='green')


    # Add title and axis names
    plt.title('Performance in termini di tempo di esecuzione')
    plt.xlabel('Dimensione (bit)')
    plt.ylabel('Tempo (us)')
    plt.xscale('log')

    ticks = []
    ticks_labels = []

    for i in range(5, 10):
        ticks.append(2**i)
        ticks_labels.append('$2^{' + str(i) + '}$')
        
    plt.xticks(ticks, ticks_labels)
    plt.legend()

    if img_filename.endswith(".pdf"):
        plt.savefig(img_filename, format="pdf")
    else:
        plt.savefig(img_filename + '.png')
    # plt.show()

    plt.yscale('log')
    if img_filename.endswith(".pdf"):
        #remove the .pdf extension to avoid duplication
        img_filename = img_filename[:-4]
        plt.savefig(img_filename + '-log.pdf', format="pdf")
    else:
        plt.savefig(img_filename + '-log.png')
    return 1

    

if __name__ == "__main__":
    # Set the style
    seabornConfig()
    

    # Create the chart
    createChart("DatiRow/RisultatiRow.csv", "Immagini/risultati.pdf")