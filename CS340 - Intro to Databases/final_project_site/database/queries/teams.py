# File name: teams.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains functions to query the database for teams data.
#       Imported and used in app.py to retrieve the data to render the teams.j2 template

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module   

# Receives database connection.
# Returns list of teams data for all teams, including team name, home city, and player count
def get_teams_data(db):
    query =  """
        SELECT Teams.team_name, Teams.team_home, COUNT(Players.player_id) as player_count
        FROM Teams
            LEFT JOIN Players 
                ON Teams.team_id = Players.team_id
        GROUP BY Teams.team_id
        ORDER BY Teams.team_id;"""  
    teams = db_module.query(dbConnection=db, query=query).fetchall()
    return teams

# Receives database connection.
# Returns list of team names and team ids for all teams, ordered alphabetically by team name
def get_list_of_teams(db):
    query = """
        SELECT team_id, team_name 
        FROM Teams
        ORDER BY team_name;"""
    team_list = db_module.query(dbConnection=db, query=query).fetchall()
    return team_list

    