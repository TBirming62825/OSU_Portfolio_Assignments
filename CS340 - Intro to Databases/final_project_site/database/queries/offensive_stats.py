# File name: offensive_stats.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains database query functions for retrieving offensive stats for all teams and their opponents.
#       Imported and used in app.py to retrieve the data to render the offensive_stats.j2 template

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection.
# Returns list of offensive stats for all teams and their opponents
def get_offensive_stats(db):
    query =  """
        SELECT 
            CONCAT(p.first_name, " ", p.last_name) AS Name,
            t.team_name AS Team, 
            t_op.team_name AS Opponent,
            CONCAT(so.pass_complete,"/",so.pass_attempt) AS pass_ca,
            so.pass_yards,
            so.pass_touchdown, 
            so.pass_interception, 
            so.rush_attempt, 
            so.rush_yard, 
            so.rush_touchdown, 
            CONCAT(so.receiving_reception,"/",so.receiving_target) AS receiving_rt,
            so.receiving_yard,
            so.receiving_touchdown,
            so.two_point_conversion,
            so.fumble
        FROM StatsOffensive as so
        INNER JOIN Teams as t
            ON so.team_id = t.team_id
        INNER JOIN Games as g
            ON so.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.home_team_id = t_op.team_id
        LEFT JOIN Players as p
            ON so.player_id = p.player_id
        WHERE so.team_id != g.home_team_id
        
        UNION ALL
        
        SELECT 
            CONCAT(p.first_name, " ", p.last_name) AS Name,
            t.team_name AS Team, 
            t_op.team_name AS Opponent,
            CONCAT(so.pass_complete,"/",so.pass_attempt) AS pass_ca,
            so.pass_yards,
            so.pass_touchdown, 
            so.pass_interception, 
            so.rush_attempt, 
            so.rush_yard, 
            so.rush_touchdown, 
            CONCAT(so.receiving_reception,"/",so.receiving_target) AS receiving_rt,
            so.receiving_yard,
            so.receiving_touchdown,
            so.two_point_conversion,
            so.fumble
        FROM StatsOffensive as so
        INNER JOIN Teams as t
            ON so.team_id = t.team_id
        INNER JOIN Games as g
            ON so.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.away_team_id = t_op.team_id
        LEFT JOIN Players as p
            ON so.player_id = p.player_id
        WHERE so.team_id != g.away_team_id
        ORDER BY Name
        """
    offensive_stats = db_module.query(dbConnection=db, query=query).fetchall()
    return offensive_stats