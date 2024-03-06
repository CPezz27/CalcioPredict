
import requests
import os
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from datetime import datetime


app = Flask(__name__)
app.secret_key = '358DHFJASN8358923ANFU835'

# Caricamento dei dati
# Stagione 2023-2024
year = "2324"
# I1.csv - Italia
# SP1.csv - Spagna
# F1.csv - Francia
# D1.csv - Germania
# E0.csv - Inghilterra
league = "I1.csv"

url = 'https://www.football-data.co.uk/mmz4281/' + year + '/' + league

# Ottieni la data odierna
today = datetime.today().date()

# Crea il nome del file da salvare nella cartella dello script
file_name = os.path.join(os.path.dirname(__file__), league)

# Controlla se il file esiste e se la data dell'ultima modifica è stata fatta oggi
if os.path.exists(file_name):
    modification_time = datetime.fromtimestamp(os.path.getmtime(file_name)).date()
    if modification_time == today:
        print("Il file è stato già scaricato nella data odierna.\n")
    else:
        # Scarica il file
        response = requests.get(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print("File scaricato con successo!\n")
else:
    # Scarica il file se non esiste
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print("File scaricato con successo!\n")




if __name__ == '__main__':
    app.run()
