#tool per farei i grafici
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def seabornConfig():
    # Set the style
    sns.set_style("whitegrid")

def df_to_latex_data_only(df, float_fmt=".3f"):
    """
    Stampa i dati del DataFrame in formato LaTeX, inclusi i nomi delle colonne.
    I float interi vengono stampati senza decimali, gli altri secondo il formato specificato.
    """
    # Header (nomi delle colonne)
    header = " & ".join(df.columns.astype(str)) + r" \\"
    print(header)

    # Riga per riga
    for _, row in df.iterrows():
        latex_row = []
        for item in row:
            if isinstance(item, float):
                if item.is_integer():
                    latex_row.append(f"{int(item)}")
                else:
                    latex_row.append(format(item, float_fmt))
            else:
                latex_row.append(str(item))
        print(" & ".join(latex_row) + r" \\")

def createChart(filename, img_filename):
    plt.clf()
    
    x_values = 8
    
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

    df_complete = df[df['platform'] == 'RP2350']
    df_math = df[df['platform'] == 'RP2350-NOMATH']
    df_transpose = df[df['platform'] == 'RP2350-NOTRANSPOSE']
    df_memory = df[df['platform'] == 'RP2350-ONLYMEMORY']
    
    # Copia le colonne 'ComputazioneSerialeFast' dei tre df nuovi in df
    df_complete.loc[:, 'mathTime'] = df_math['ComputazioneSerialeFast'].values
    df_complete.loc[:, 'transposeTime'] = df_transpose['ComputazioneSerialeFast'].values
    df_complete.loc[:, 'memoryTime'] = df_memory['ComputazioneSerialeFast'].values
    
    df_complete['math'] = df_complete['ComputazioneSerialeFast'] - df_complete['mathTime']
    df_complete['transpose'] = df_complete['ComputazioneSerialeFast'] - df_complete['transposeTime']
    # df_complete['memory'] = df_complete['ComputazioneSerialeFast'] - df_complete['memoryTime']
    
    # Calcolo le percentuali
    df_complete['mathPercent'] = df_complete['math'] / df_complete['ComputazioneSerialeFast'] * 100
    df_complete['transposePercent'] = df_complete['transpose'] / df_complete['ComputazioneSerialeFast'] * 100
    df_complete['memoryPercent'] = df_complete['memoryTime'] / df_complete['ComputazioneSerialeFast'] * 100
    # df_complete['otherPercent'] = 100 - df_complete['mathPercent'] - df_complete['transposePercent'] - df_complete['memoryPercent']
    
    df_long = df_complete.melt(id_vars='size(bit)', var_name='task', value_name='percent')
    
    #Filtra solo le righe che contengono le percentuali
    df_long = df_long[df_long['task'].str.contains('Percent')]
    
    
    pivot_df = df_long.pivot(index='size(bit)', columns='task', values='percent')
    
    # Creo un diagramma a barre con le percentuali usando seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df.plot(kind='bar', stacked=True, ax=ax)
    
    print(pivot_df)
    
    plt.xticks(rotation=0)
    # plt.xlabel('Dimensione (bit)')
    # plt.ylabel('Percentuale (%)')
    plt.title('Percentuale di tempo di esecuzione per task')
    # plt.suptitle('ComputazioneSerialeFast - Barre Impilate per Dimensione (bit)', fontsize=14, y=1.08)
    # plt.legend(
    #     title='Piattaforma',
    #     bbox_to_anchor=(0.5, 1.15),
    #     loc='upper center',
    #     ncol=2,
    # )
    
    ax.set_ylabel('Valore')
    ax.set_xlabel('Dimensione (bit)')
    
    legend_labels = {
        'mathPercent': 'Computazione',
        'transposePercent': 'Trasposizione',
        'memoryPercent': 'Memoria',
    }

    # Recupera i handle (colore) e label (nome originale)
    handles, labels = ax.get_legend_handles_labels()

    # Applica la mappatura solo alla legenda
    new_labels = [legend_labels.get(label, label) for label in labels]
    ax.legend(handles, labels=new_labels, title='Piattaforma', bbox_to_anchor=(1.02, 1), loc='upper left',borderaxespad=0.)    
    
    plt.tight_layout()
    plt.savefig(img_filename + '.png')
    plt.savefig(img_filename + '.pdf')
        
    
    
    return 1

    

if __name__ == "__main__":
    # Set the style
    seabornConfig()
    

    # Create the chart
    createChart("DatiRow/RisultatiAI.csv", "Immagini/AI")