# File name: players.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains database query functions for retrieving player data for all teams.
#       Imported and used in app.py to retrieve the data to render the players.j2 template

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection 
# Returns list of players data for all teams, including player name, team name, and position
def get_players_data(db):
    query =  """
        SELECT CONCAT(Players.first_name, " ", Players.last_name) as Name, Teams.team_name AS Team, Players.position AS Position
        FROM Players
            LEFT JOIN Teams
            ON Players.team_id = Teams.team_id
        ORDER BY Team, Position DESC
        """
    players = db_module.query(dbConnection=db, query=query).fetchall()
    return players

