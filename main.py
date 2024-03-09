import requests
import os
from flask import flask, jsonify, request, render_template, session, redirect, url_for
from team import Team
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

data = pd.read_csv(file_name)

# Pulizia dei dati: mantengo solo le colonne che mi interessano. In particolare abbiamo:
# Date -> Data della partita (gg/mm/aaaa); HomeTeam -> Squadra casa; 'AwayTeam' -> Squadra ospite,
# FTHG -> Squadra casa goal finali; FTAG -> Squadra ospite goal finali
# FTR' -> Risultato finale (H -> casa; D -> pareggio; L -> ospite)
# HTHG -> Squadra casa goal primo tempo; HTAG -> Squadra casa goal primo tempo
# HTR -> Risultato primo tempo (H -> casa; D -> pareggio; L -> ospite)
# HS -> Tiri squadra casa; AS -> Tiri squadra ospite
# HST -> Tiri in porta casa;  AST -> Tiri in porta ospite
# HF -> Falli commessi casa; AF -> Falli commessi ospite
# HC -> Calci d'angolo casa; AC -> Calci d'angolo ospite
# HY -> Cartellini gialli casa; AY -> Cartellini gialli ospite
# HR -> Cartellini rossi casa; AR ->Cartellini rossi ospite

data = data[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS',
             'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]

teams = pd.unique(data[['HomeTeam', 'AwayTeam']].values.ravel('K'))
teams.sort()

teamsList = []

print("Sto creando i singoli team e sto calcolando le statistiche.")

for team in tqdm(teams):
    t = Team(team)

    home_team = data[data['HomeTeam'] == team]
    away_team = data[data['AwayTeam'] == team]

    matches = pd.concat([home_team, away_team]).drop_duplicates()

    t.home_matches = len(home_team)
    t.home_wins = len(home_team[home_team['FTR'] == 'H'])
    t.home_draws = len(home_team[home_team['FTR'] == 'D'])
    t.home_losses = len(home_team[home_team['FTR'] == 'A'])
    t.home_goals_for = matches[matches['HomeTeam'] == team]['FTHG'].sum()
    t.home_goals_against = matches[matches['HomeTeam'] == team]['FTAG'].sum()
    t.home_shots = matches[matches['HomeTeam'] == team]['HS'].sum()
    t.home_shots_target = matches[matches['HomeTeam'] == team]['HST'].sum()
    t.home_fouls_committed = matches[matches['HomeTeam'] == team]['HF'].sum()
    t.home_total_corners = matches[matches['HomeTeam'] == team]['HC'].sum()
    t.home_yellow_cards = matches[matches['HomeTeam'] == team]['HY'].sum()
    t.home_red_cards = matches[matches['HomeTeam'] == team]['HR'].sum()

    t.away_matches = len(away_team)
    t.away_wins = len(away_team[away_team['FTR'] == 'A'])
    t.away_draws = len(away_team[away_team['FTR'] == 'D'])
    t.away_losses = len(away_team[away_team['FTR'] == 'H'])
    t.away_goals_for = matches[matches['AwayTeam'] == team]['FTAG'].sum()
    t.away_goals_against = matches[matches['AwayTeam'] == team]['FTHG'].sum()
    t.away_shots = matches[matches['AwayTeam'] == team]['AS'].sum()
    t.away_shots_target = matches[matches['AwayTeam'] == team]['AST'].sum()
    t.away_fouls_committed = matches[matches['AwayTeam'] == team]['AF'].sum()
    t.away_total_corners = matches[matches['AwayTeam'] == team]['AC'].sum()
    t.away_yellow_cards = matches[matches['AwayTeam'] == team]['AY'].sum()
    t.away_red_cards = matches[matches['AwayTeam'] == team]['AR'].sum()

    t.points = ((t.home_wins + t.away_wins) * 3 + (t.home_draws + t.away_draws) * 1) * 0.8

    t.average_goals_away = t.home_matches / t.home_goals_for
    t.average_goals_home = t.away_matches / t.away_goals_for

    t.matches = t.home_matches + t.away_matches

    teamsList.append(t)

# Crea un DataFrame vuoto per immagazzinare i valori aggregati

new_data = pd.DataFrame(columns=['HomeTeam', 'h_home_goals_for', 'h_away_goals_for', 'h_home_goals_against',
                                 'h_away_goals_against', 'h_home_shots_target', 'h_away_shots_target',
                                 'h_home_red_cards', 'h_away_red_cards',
                                 'AwayTeam', 'a_home_goals_for', 'a_away_goals_for', 'a_home_goals_against',
                                 'a_away_goals_against', 'a_home_shots_target', 'a_away_shots_target',
                                 'a_home_red_cards', 'a_away_red_cards' 'result'])

rows_to_add = []

print("\nCreando il nuovo dataframe per i modelli di machine learning e deep learning...")

# Ciclo per ottenere le somme cumulative
for idx, row in tqdm(data.iterrows()):
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']

    # home
    h_home_goals_for = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'FTHG'].sum()
    h_home_goals_against = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'FTAG'].sum()
    h_home_shots_target = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'HST'].sum()
    h_home_red_cards = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'HR'].sum()
    h_home_shots = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'HS'].sum()
    h_home_fouls_committed = data.loc[data['HomeTeam'] == home_team].loc[:idx, 'HF'].sum()

    h_away_goals_for = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'FTAG'].sum()
    h_away_goals_against = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'FTHG'].sum()
    h_away_shots_target = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'AST'].sum()
    h_away_red_cards = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'AR'].sum()
    h_away_shots = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'AS'].sum()
    h_away_fouls_committed = data.loc[data['AwayTeam'] == home_team].loc[:idx, 'AF'].sum()

    # away
    a_home_goals_for = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'FTHG'].sum()
    a_home_goals_against = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'FTAG'].sum()
    a_home_shots_target = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'HST'].sum()
    a_home_red_cards = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'HR'].sum()
    a_home_shots = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'HS'].sum()
    a_home_fouls_committed = data.loc[data['HomeTeam'] == away_team].loc[:idx, 'HF'].sum()

    a_away_goals_for = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'FTAG'].sum()
    a_away_goals_against = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'FTHG'].sum()
    a_away_shots_target = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'AST'].sum()
    a_away_red_cards = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'AR'].sum()
    a_away_shots = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'AS'].sum()
    a_away_fouls_committed = data.loc[data['AwayTeam'] == away_team].loc[:idx, 'AF'].sum()

    # 001 -> H / 010 -> D / 100 -> A
    result = row['FTR']

    if result == 'H':
        result = "001"
    elif result == 'D':
        result = "010"
    elif result == 'A':
        result = "100"

    # Creazione di una nuova riga con i valori aggregati
    new_row = {
        'HomeTeam': one_hot_encode_team(home_team, teams),
        'h_home_goals_for': h_home_goals_for, 'h_away_goals_for': h_away_goals_for,
        'h_home_goals_against': h_home_goals_against, 'h_away_goals_against': h_away_goals_against,
        'h_home_shots_target': h_home_shots_target, 'h_away_shots_target': h_away_shots_target,
        'h_home_red_cards': h_home_red_cards, 'h_away_red_cards': h_away_red_cards,
        'h_home_shots': h_home_shots, 'h_away_shots': h_away_shots,
        'h_home_fouls_committed': h_home_fouls_committed, 'h_away_fouls_committed': h_away_fouls_committed,
        'AwayTeam': one_hot_encode_team(away_team, teams),
        'a_home_goals_for': a_home_goals_for, 'a_away_goals_for': a_away_goals_for,
        'a_home_goals_against': a_home_goals_against, 'a_away_goals_against': a_away_goals_against,
        'a_home_shots_target': a_home_shots_target, 'a_away_shots_target': a_away_shots_target,
        'a_home_red_cards': a_home_red_cards, 'a_away_red_cards': a_away_red_cards,
        'a_home_shots': a_home_shots, 'a_away_shots': a_away_shots,
        'a_home_fouls_committed': a_home_fouls_committed, 'a_away_fouls_committed': a_away_fouls_committed,
        'result': result
    }

    # Aggiunta della riga al nuovo DataFrame
    rows_to_add.append(new_row)

print("")


if __name__ == '__main__':
    app.run()
