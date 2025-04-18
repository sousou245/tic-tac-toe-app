import random
from pymongo import MongoClient

# ------------------------------
# 1. Connexion à MongoDB
# ------------------------------
client = MongoClient('mongodb://localhost:27017/')
db = client['tic_tac_toe_db']
players_collection = db['players']
history_collection = db['history']

# ------------------------------
# 2. Fonctions utilitaires
# ------------------------------

def display_board(board):
    """Affiche le plateau de jeu."""
    print("\n")
    for i in range(3):
        print(" | ".join(board[i * 3:(i + 1) * 3]))
        if i < 2:
            print("-" * 5)


def check_winner(board):
    """Vérifie si un joueur a gagné."""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
        [0, 4, 8], [2, 4, 6]             # Diagonales
    ]
    for combo in winning_combinations:
        if board[combo[0]] != " " and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return None


def update_score(player_name, result):
    """Met à jour le score du joueur en fonction du résultat."""
    increment = 1 if result == "win" else 0
    players_collection.update_one({"name": player_name}, {"$inc": {"score": increment}})


def display_leaderboard():
    """Affiche le classement des meilleurs joueurs."""
    print("\n--- Leaderboard ---")
    top_players = players_collection.find().sort("score", -1).limit(3)
    for player in top_players:
        print(f"{player['name']}: {player['score']} points")
    print("-------------------\n")


def display_history(player_name):
    """Affiche l'historique des parties d'un joueur."""
    print(f"\n--- Historique des parties de {player_name} ---")
    games = history_collection.find({"player": player_name})
    for game in games:
        print(f"Plateau: {game['board']}, Gagnant: {game['winner']}")
    print("---------------------------------------------\n")

# ------------------------------
# 3. Algorithme Minimax
# ------------------------------

def minimax(board, depth, is_maximizing):
    """Implémente l'algorithme Minimax pour trouver le meilleur coup."""
    winner = check_winner(board)
    if winner == "O":
        return 1  # L'ordinateur gagne
    elif winner == "X":
        return -1  # Le joueur gagne
    elif " " not in board:
        return 0  # Match nul

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


def best_move(board):
    """Trouve le meilleur coup pour l'ordinateur."""
    best_score = float('-inf')
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ------------------------------
# 4. Fonction principale
# ------------------------------

def main():
    """Fonction principale du jeu Tic Tac Toe."""
    print("Bienvenue au jeu de Tic Tac Toe !")
    display_leaderboard()

    # Enregistrement du joueur
    player_name = input("Entrez votre nom : ").strip()
    player = players_collection.find_one({"name": player_name})
    if not player:
        print(f"Bienvenue, {player_name} ! Votre score initial est 0.")
        players_collection.insert_one({"name": player_name, "score": 0})
    else:
        print(f"Re-bonjour, {player_name} ! Votre score actuel est {player['score']}.")

    # Afficher l'historique si demandé
    if input("Voulez-vous voir votre historique des parties ? (oui/non) : ").lower() == "oui":
        display_history(player_name)

    # Initialisation du plateau
    board = [" "] * 9
    current_player = "X"  # Le joueur commence

    while True:
        display_board(board)

        if current_player == "X":
            try:
                move = int(input("Choisissez une case (0-8) : "))
                if board[move] == " ":
                    board[move] = "X"
                else:
                    print("Case déjà occupée ! Essayez encore.")
                    continue
            except (ValueError, IndexError):
                print("Entrée invalide ! Choisissez un chiffre entre 0 et 8.")
                continue

        elif current_player == "O":
            print("L'ordinateur réfléchit...")
            move = best_move(board)
            if move != -1:
                board[move] = "O"

        winner = check_winner(board)
        if winner:
            display_board(board)
            if winner == "X":
                print("Félicitations ! Vous avez gagné !")
                update_score(player_name, "win")
            else:
                print("L'ordinateur a gagné !")
                update_score(player_name, "lose")

            history_collection.insert_one({"player": player_name, "board": board, "winner": winner})
            break

        current_player = "O" if current_player == "X" else "X"

    print("Merci d'avoir joué !")

if __name__ == "__main__":
    main()
