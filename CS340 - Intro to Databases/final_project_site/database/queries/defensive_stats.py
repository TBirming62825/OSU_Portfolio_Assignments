# File name: defensive_stats.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains database query function for retrieving defensive stats for all teams and their opponents.
#       Imported and used in app.py to retrieve the data to render the defensive_stats.j2 template

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology)and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors


import database.db_connector as db_module

# Receives database connection.
# Returns list of defensive stats for all teams and their opponents
def get_defensive_stats(db):

    # Need to use a UNION ALL to combine the results for home and away games, 
    # since opponent team is stored in different columns in the Games table depending on whether the team is playing at home or away
    query =  """
        SELECT 
            t.team_name AS Team,
            t_op.team_name AS Opponent,
            sd.points_allowed,
            sd.yards_allowed,
            sd.sack,
            sd.fumble_recover,
            sd.defensive_interception,
            sd.defensive_touchdown,
            sd.blocked_punt,
            sd.safety
        FROM StatsDefensive as sd
        INNER JOIN Teams as t
            ON sd.team_id = t.team_id
        INNER JOIN Games as g
            ON sd.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.home_team_id = t_op.team_id
        WHERE sd.team_id != g.home_team_id
        
        UNION ALL

        SELECT 
            t.team_name AS Team,
            t_op.team_name AS Opponent,
            sd.points_allowed,
            sd.yards_allowed,
            sd.sack,
            sd.fumble_recover,
            sd.defensive_interception,
            sd.defensive_touchdown,
            sd.blocked_punt,
            sd.safety
        FROM StatsDefensive as sd
        INNER JOIN Teams as t
            ON sd.team_id = t.team_id
        INNER JOIN Games as g
            ON sd.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.away_team_id = t_op.team_id
        WHERE sd.team_id != g.away_team_id
        """
    defensive_stats = db_module.query(dbConnection=db, query=query).fetchall()   
    return defensive_stats