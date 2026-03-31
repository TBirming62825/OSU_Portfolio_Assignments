# # File name: games.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains database query functions for retrieving games data, player games data, deleting a game, and creating a game.
#       Imported and used in app.py to retrieve the data to render the games.j2 template, and to handle the delete and create game functionality

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection.
# Returns a list of games data, including home team, away team, points scored, week number, year, and game id
def get_games_data(db):
    query =  """
        SELECT  t_home.team_name AS home_team,
                Games.home_points_scored,
                t_away.team_name AS away_team,
                Games.away_points_scored,
                Games.week_number,
                Games.year,
                Games.game_id
        FROM Games
        JOIN Teams t_home
            ON Games.home_team_id = t_home.team_id
        JOIN Teams t_away
            ON Games.away_team_id = t_away.team_id
        """
    games = db_module.query(dbConnection=db, query=query).fetchall()
    return games

# Receives database connection and a player id. 
# Returns list of that player's games, includes  home team, away team, week number, year, and game id. 
# Only returns games for players in the kicker position who do not have stats recorded for that game in the StatsKicker table
def get_player_games(db, player_id):
    player_games_query = """
        SELECT 
            g.game_id,
            g.week_number,
            g.year,
            t_a.team_name AS away_team,
            t_a.team_id As away_team_id,
            t_h.team_name AS home_team,
            t_h.team_id As home_team_id
        FROM Games AS g
        INNER JOIN Teams AS t_a
            ON g.away_team_id = t_a.team_id
        INNER JOIN Teams AS t_h
            ON g.home_team_id = t_h.team_id
        INNER JOIN Players AS p
            ON p.player_id = %s
        WHERE p.position = 'K'
            AND (p.team_id = g.home_team_id OR p.team_id = g.away_team_id)
            AND NOT EXISTS (
            SELECT 1
            FROM StatsKicker as sk
            WHERE sk.game_id = g.game_id
                AND sk.player_id = %s)
        ORDER BY g.year, g.week_number;
        """
    player_games = db_module.query(dbConnection=db, query=player_games_query, query_params=(player_id, player_id)).fetchall()
    return player_games

# Receives database connection and a game id. 
# Deletes that game from the database by calling the sp_DeleteGame stored procedure
def delete_game_query(db, game_id):
    game_id = int(game_id)

    # Using parameterized queries (Prevents SQL injection attacks) Call on the sp_DeleteGame
    query = "CALL sp_DeleteGame(%s)"
    cursor = db_module.query(dbConnection=db, query=query, query_params=(game_id,))
    while cursor.nextset():
        pass
    cursor.close()

# Receives database connection and the data for a new game (home team id, home points scored, away team id, away points scored, week number, year).
# Creates a new game in the database by calling the sp_CreateGame stored procedure with the given data
def create_game_query(db, home_team_id, home_points_scored, away_team_id, away_points_scored, week_number, year):
    
    # Using parameterized queries (Prevents SQL injection attacks) Call on the sp_CreateGame
    query = "CALL sp_CreateGame(%s, %s, %s, %s, %s, %s)"
    cursor = db_module.query(dbConnection=db, query=query, query_params=(home_team_id, home_points_scored, 
                                away_team_id, away_points_scored, week_number, year))
    while cursor.nextset():
        pass
    cursor.close()  