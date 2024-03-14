import numpy


class Team:
    def __init__(self, name: str):
        self.name = name
        self.matches = 0
        # Goal fatti e subiti in casa
        self.home_goals_for = 0
        self.home_goals_against = 0
        # Goal fatti e subiti da ospite
        self.away_goals_for = 0
        self.away_goals_against = 0
        # Vittorie, sconfitte e pareggi in casa
        self.home_wins = 0
        self.home_losses = 0
        self.home_draws = 0
        # Vittorie, sconfitte e pareggi da ospite
        self.away_wins = 0
        self.away_losses = 0
        self.away_draws = 0
        # Numero di match giocati in casa e da ospite
        self.home_matches = 0
        self.away_matches = 0
        # Numero totale di tiri da ospite [AS]
        self.away_shots = 0
        # Numero di tiri nello specchio della porta da ospite [AST]
        self.away_shots_target = 0
        # Numero totale di tiri da ospite [HS]
        self.home_shots = 0
        # Numero di tiri nello specchio della porta da ospite [HST]
        self.home_shots_target = 0

        # Numero totale di falli fatti in casa [HF]
        self.home_fouls_committed = 0
        # Numero totale di falli fatti da ospite [AF]
        self.away_fouls_committed = 0
        # Numero totale di calci d'angolo in casa [HC]
        self.home_total_corners = 0
        # Numero totale di calci d'angolo da ospite [AC]
        self.away_total_corners = 0
        # Numero totale di cartellini gialli in casa [HY]
        self.home_yellow_cards = 0
        # Numero totale di cartellini gialli da ospite [AY]
        self.away_yellow_cards = 0
        # Numero totale di espulsioni in casa [HR]
        self.home_red_cards = 0
        # Numero totale di espulsioni da ospite [AR]
        self.away_red_cards = 0
        # Punteggio in base al numero di partite vinte / pareggiate / perse
        self.points = 0
        # Media dei goal complessivi per le partite
        self.average_goals_away = 0
        self.average_goals_home = 0

    def get_stats(self):
        stats = (f"Team: {self.name}\n"
                 f"Points: {self.points}\n"
                 f"Matches Played: {self.matches}\n"
                 f"Matches Wins: {self.home_wins + self.away_wins}\n"
                 f"Matches Loss: {self.home_losses + self.away_losses}\n"
                 f"Matches Draws: {self.home_draws + self.away_draws}\n"
                 f"Total Goals Scored (Full Time): {self.home_goals_for + self.away_goals_for}\n"
                 f"Total Goals Conceded (Full Time): {self.home_goals_against + self.away_goals_against}\n"
                 f"Total Shots (Home): {self.home_shots}\n"
                 f"Total Shots (Away): {self.away_shots}\n"
                 f"Shots on Target (Home): {self.home_shots_target}\n"
                 f"Shots on Target (Away): {self.away_shots_target}\n"
                 f"Total Fouls Committed (Home): {self.home_fouls_committed}\n"
                 f"Total Fouls Committed (Away): {self.away_fouls_committed}\n"
                 f"Total Corners (Home): {self.home_total_corners}\n"
                 f"Total Corners (Away): {self.away_total_corners}\n"
                 f"Total Yellow Cards (Home): {self.home_yellow_cards}\n"
                 f"Total Yellow Cards (Away): {self.away_yellow_cards}\n"
                 f"Total Red Cards (Home): {self.home_red_cards}\n"
                 f"Total Red Cards (Away): {self.away_red_cards}")
        return stats
