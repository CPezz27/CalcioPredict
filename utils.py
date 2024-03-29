import math
from time import time
from sklearn.metrics import f1_score
from team import Team
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


def poisson_probability(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)


def outcome_probabilities(home_goals, away_goals):
    max_goals = max(len(home_goals), len(away_goals))

    home_win_prob = 0
    draw_prob = 0
    away_win_prob = 0

    for i in range(max_goals):
        for j in range(max_goals):
            if i < len(home_goals) and j < len(away_goals):
                prob = home_goals[i] * away_goals[j]
                if i > j:
                    home_win_prob += prob
                elif i == j:
                    draw_prob += prob
                else:
                    away_win_prob += prob
    return home_win_prob, draw_prob, away_win_prob


def calculate_home_win_probability(home_team: Team, away_team: Team):
    # Probabilità di vittoria in casa basata sulle statistiche delle due squadre
    home_win_prob = (home_team.home_wins / home_team.home_matches) - (away_team.away_losses / away_team.away_matches)
    return home_win_prob * 100


def calculate_away_win_probability(home_team: Team, away_team: Team):
    # Probabilità di vittoria in trasferta basata sulle statistiche delle due squadre
    away_win_prob = (away_team.away_wins / away_team.away_matches) - (home_team.home_losses / home_team.home_matches)
    return away_win_prob * 100


def calculate_draw_probability(home_team: Team, away_team: Team):
    # Probabilità di pareggio basata sulle statistiche delle due squadre
    home_draw_prob = home_team.home_draws / home_team.home_matches
    away_draw_prob = away_team.away_draws / away_team.away_matches
    draw_prob = (home_draw_prob + away_draw_prob) / 2  # Media delle probabilità di pareggio delle due squadre
    return draw_prob * 100


def one_hot_encode_team(team_name, teams):
    teams_list = teams.tolist() if isinstance(teams, np.ndarray) else teams
    encoding = [0] * len(teams_list)
    if team_name in teams_list:
        team_idx = teams_list.index(team_name)
        encoding[team_idx] = 1
    encoding_string = ''.join(map(str, encoding))
    return encoding_string


def calculate_voting_classifier_accuracy(random_state, X, Y):
    X_train_voting, X_test_voting, Y_train_voting, Y_test_voting = train_test_split(X, Y, test_size=0.2,
                                                                                    random_state=random_state)

    scaler_voting = StandardScaler()
    X_train_voting = scaler_voting.fit_transform(X_train_voting.values)
    X_test_voting = scaler_voting.transform(X_test_voting.values)

    clf1 = RandomForestClassifier(max_depth=7, max_features='sqrt', max_leaf_nodes=8, n_estimators=170)
    clf2 = LogisticRegression(max_iter=10000)
    clf3 = SVC(C=5, gamma='scale')

    eclf = VotingClassifier(estimators=[('rf', clf1), ('lr', clf2), ('svc', clf3)], voting='hard')

    eclf.fit(X_train_voting, Y_train_voting)

    Y_pred = eclf.predict(X_test_voting)

    return scaler_voting, eclf, accuracy_score(Y_test_voting, Y_pred)