import pymongo

# Connexion à MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tic_tac_toe_db"]
players_collection = db["players"]
history_collection = db["history"]

# Récupère ou crée un joueur
def get_or_create_player(player_name):
    player = players_collection.find_one({"name": player_name})
    if not player:
        players_collection.insert_one({"name": player_name, "score": 0})
        return {"name": player_name, "score": 0}
    return player

# Met à jour le score d'un joueur
def update_score(player_name, increment):
    players_collection.update_one(
        {"name": player_name}, {"$inc": {"score": increment}}
    )

# Sauvegarde l'historique des parties
def save_game_history(player_name, board, winner):
    history_collection.insert_one(
        {"player": player_name, "board": board, "winner": winner}
    )

# Récupère les 3 meilleurs joueurs du leaderboard
def get_leaderboard():
    return list(players_collection.find().sort("score", -1).limit(3))

# Récupère l'historique des parties d'un joueur
def get_player_history(player_name):
    return list(history_collection.find({"player": player_name}))

