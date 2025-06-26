#!bin/bash
# Creare un ambiente virtuale per python con le librerie necessarie per l'analisi dei risultati.

#Variabili di ambiente
PYTHON_ENV_DIR=.venv

export PYTHON_ENV_DIR=$PYTHON_ENV_DIR

#Creazione dell'ambiente virtuale
if [ ! -d "$PYTHON_ENV_DIR" ]; then
    echo "Creazione dell'ambiente virtuale in $PYTHON_ENV_DIR"
    python3 -m venv $PYTHON_ENV_DIR
else
    echo "L'ambiente virtuale esiste già in $PYTHON_ENV_DIR"
fi

#Attivazione dell'ambiente virtuale
source $PYTHON_ENV_DIR/bin/activate

#Aggiornamento di pip all'ultima versione
echo "Aggiornamento di pip all'ultima versione"
pip install --upgrade pip

#Installazione delle librerie necessarie
pip install pandas matplotlib seaborn

#Disattivazione enviroment
deactivate