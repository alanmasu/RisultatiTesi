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

    # Controllo che le colonne siano presenti    
    df['BTPU'] = df['Caricamento'] + df['Settaggio'] + df['Inizializzazione'] + df['ComputazioneBTPU'] + df['LetturaRisultato']
    
    # Calcolo dello speedup
    df['Speedup'] = df['ComputazioneSerialeFast'] / df['BTPU']
    
    # Calcolo dell'influenza della BTPU in termini di tempo di computazione
    df['AI'] = df['ComputazioneBTPU'] / df['BTPU'] * 100
    
    # Filtro le colonne che mi interessano
    df_selected = df[['size(bit)', 'platform', 'BTPU', 'ComputazioneSerialeFast', 'Speedup', 'AI']]
    
    # Pivot della tabella
    df_wide = df_selected.pivot_table(index="size(bit)", columns="platform")

    # Appiattisco le colonne (MultiIndex -> stringhe tipo 'latency_CPU')
    df_wide.columns = [f"{col[0]}_{col[1]}" for col in df_wide.columns]

    # Rendo 'size(bit)' una colonna normale
    df_wide = df_wide.reset_index()
    
    # Printo il dataframe in formato LaTeX
    df_to_latex_data_only(df_wide)
    
    # print(df_wide)
    
    
    df_FPGA = df[df['platform'] == 'FPGA']
    df_RP2350 = df[df['platform'] == 'RP2350']
    
    df_RP2350.loc[:, 'ComputazioneBTPU'] = df_FPGA['ComputazioneBTPU'].values
    
    sns.lineplot(x='size(bit)', y='ComputazioneSerialeFast', data=df_FPGA, label='$t_s$ (FPGA)', color='blue')
    sns.lineplot(x='size(bit)', y='ComputazioneSerialeFast', data=df_RP2350, label='$t_s$ (RP2350)', color='orange')
    sns.lineplot(x='size(bit)', y='BTPU', data=df_FPGA, label='$t_p$ (FPGA)', color='red')
    sns.lineplot(x='size(bit)', y='BTPU', data=df_RP2350, label='$t^{*}_{p}$ (RP2350)', color='green')


    # Add title and axis names
    plt.title('Performance in termini di tempo di esecuzione')
    plt.xlabel('Dimensione (bit)')
    plt.ylabel('Tempo (us)')
    plt.xscale('log', base=2)

    ticks = []
    ticks_labels = []

    for i in range(5, 9):
        ticks.append(2**i)
        ticks_labels.append('$2^{' + str(i) + '}$')
        
    plt.xticks(ticks, ticks_labels)
    # plt.xlim(2**5, 2**8)
    plt.legend()

    plt.savefig(img_filename + '.pdf', format="pdf")
    plt.savefig(img_filename + '.png')
    # plt.show()

    plt.yscale('log')
    plt.savefig(img_filename + '-log.pdf', format="pdf")
    plt.savefig(img_filename + '-log.png')
                
    ## Plotting the speedup
    plt.clf()
        
    sns.lineplot(x='size(bit)', y='Speedup', data=df_FPGA, label='$t_{s}/t_{p}$ (FPGA)', color='blue')
    sns.lineplot(x='size(bit)', y='Speedup', data=df_RP2350, label='$t_{s}/t_{p}^{*}$ (RP2350)', color='red')
    
    plt.title('Speedup')
    
    plt.xlabel('Dimensione (bit)')
    plt.ylabel('')
    
    plt.xscale('log', base=2)
    ticks = []
    ticks_labels = []
    for i in range(5, 9):
        ticks.append(2**i)
        ticks_labels.append('$2^{' + str(i) + '}$')
    
    plt.xticks(ticks, ticks_labels)    
    
    plt.legend()
    plt.savefig(img_filename + '-speedup.pdf', format="pdf")
    plt.savefig(img_filename + '-speedup.png')
        
    plt.yscale('log')
    plt.savefig(img_filename + '-speedup-log.pdf', format="pdf")
    plt.savefig(img_filename + '-speedup-log.png')
        
    # Plot arithmetic intensity
    plt.clf()
    sns.lineplot(x='size(bit)', y='AI', data=df_FPGA, label='AI BTPU', color='blue')
    sns.lineplot(x='size(bit)', y='AI', data=df_RP2350, label='AI RP2350', color='red')
    
    plt.title('AI (Arithmetic Intensity)')
    
    plt.xlabel('Dimensione (bit)')
    plt.ylabel('')
    
    plt.xscale('log', base=2)
    ticks = []
    ticks_labels = []
    for i in range(5, 9):
        ticks.append(2**i)
        ticks_labels.append('$2^{' + str(i) + '}$')
    
    plt.xticks(ticks, ticks_labels)    
    
    plt.legend()
    plt.savefig(img_filename + '-AI.pdf', format="pdf")
    plt.savefig(img_filename + '-AI.png')
    
    
    return 1

    

if __name__ == "__main__":
    # Set the style
    seabornConfig()
    

    # Create the chart
    createChart("DatiRow/RisultatiRow.csv", "Immagini/risultati")