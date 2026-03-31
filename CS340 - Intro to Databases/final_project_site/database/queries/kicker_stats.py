# File name: kicker_stats.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains database query functions for retrieving kicker stats for all teams and their opponents, 
#       retrieving a single kicker stat for update, creating a new kicker stat, updating an existing kicker stat, 
#       and deleting a kicker stat.
#       Imported and used in app.py to retrieve the data to render the kicker_stats.j2 template, 
#       and to handle the create, update, and delete kicker stat functionality

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection.
# Returns list of kicker stats for all teams and their opponents
def get_kicker_stats(db):
    
    # Need to use a UNION ALL to combine the results for home and away games, 
    # since opponent team is stored in different columns in the Games table depending on whether the team is playing at home or away
    query =  """
        SELECT
            sk.kicker_stats_id,
            p.player_id,
            CONCAT(p.first_name, " ", p.last_name) AS Name,
            t.team_id,
            t.team_name AS Team, 
            t_op.team_name AS Opponent,
            CONCAT(sk.extra_point_made,"/", sk.extra_point_attempt) AS extra_point_ma, 
            CONCAT(sk.field_goal_made,"/", sk.field_goal_attempt)  AS field_goal_ma
        FROM StatsKicker as sk
        INNER JOIN Teams as t
            ON sk.team_id = t.team_id
        INNER JOIN Games as g
            ON sk.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.away_team_id = t_op.team_id
        LEFT JOIN Players as p
            ON sk.player_id = p.player_id
        WHERE sk.team_id != g.away_team_id

        UNION ALL

        SELECT
            sk.kicker_stats_id,
            p.player_id,
            CONCAT(p.first_name, " ", p.last_name) AS Name,
            t.team_id,
            t.team_name AS Team, 
            t_op.team_name AS Opponent,
            CONCAT(sk.extra_point_made,"/", sk.extra_point_attempt) AS extra_point_ma, 
            CONCAT(sk.field_goal_made,"/", sk.field_goal_attempt)  AS field_goal_ma
        FROM StatsKicker as sk
        INNER JOIN Teams as t
            ON sk.team_id = t.team_id
        INNER JOIN Games as g
            ON sk.game_id = g.game_id
        LEFT JOIN Teams as t_op
            ON g.home_team_id = t_op.team_id
        LEFT JOIN Players as p
            ON sk.player_id = p.player_id
        WHERE sk.team_id != g.home_team_id
        ORDER BY Name
        """  
    kicker_stats = db_module.query(dbConnection=db, query=query).fetchall()   
    return kicker_stats

# Receives database connection and a kicker stat id.
# Returns that kicker stat's data, including player name, team, opponent, extra points made/attempted, and field goals made/attempted.
def get_kicker_stats_for_update(db, id):
    query = """
        SELECT sk.kicker_stats_id, CONCAT(p.first_name, " ", p.last_name) as name, home.team_name as team, away.team_name as opponent, 
                sk.extra_point_made, sk.extra_point_attempt, sk.field_goal_made, sk.field_goal_attempt, sk.kicker_stats_id
            FROM Players as p
                INNER JOIN StatsKicker as sk 
                    ON p.player_id = sk.player_id
                INNER JOIN Games as g
                    ON sk.game_id = g.game_id
                INNER JOIN  Teams as home
                    ON g.home_team_id = home.team_id
                INNER JOIN Teams as away
                    ON g.away_team_id = away.team_id
                WHERE sk.kicker_stats_id = %s
                """
    kicker_stats = db_module.query(dbConnection=db, query=query, query_params=(id,)).fetchone()
    return kicker_stats

# Receives database connection and the data for a new kicker stat.
# Creates a new kicker stat in the database by calling the sp_CreateKickerStat stored procedure with the given data
def create_kicker_stats_query(db, a_kicker_id, a_week, a_year, a_home_team_id, a_away_team_id, a_extra_point_made, a_extra_point_attempt, a_field_goal_made, a_field_goal_attempt):
    a_game_id_query = """SELECT game_id FROM Games WHERE home_team_id = %s AND away_team_id = %s AND week_number = %s AND year = %s"""
    a_game_id = db_module.query(dbConnection=db, query=a_game_id_query, query_params=(a_home_team_id, a_away_team_id, a_week, a_year)).fetchall()
    
    # Check to ensure a game id is returned
    if not a_game_id:
        raise ValueError(f"No game found for home_team_id={a_home_team_id}, away_team_id={a_away_team_id}, week={a_week}, year={a_year}")
    a_game_id = a_game_id[0]['game_id']
    a_team_id_query = """
                SELECT team_id
                FROM Players
                WHERE player_id = %s
                """
    a_team_id = db_module.query(dbConnection=db, query=a_team_id_query, query_params=(a_kicker_id, )).fetchall()
    
    # Check to ensure a team id is returned
    if not a_team_id:
        raise ValueError("No game found")
    a_team_id = a_team_id[0]['team_id']

    # Using parameterized queries (Prevents SQL injection attacks) Call on the sp_DeleteKickerStat
    query = "CALL sp_CreateKickerStat(%s, %s, %s, %s, %s, %s, %s)"
    cursor = db_module.query(dbConnection=db, query=query, query_params=(a_game_id, a_team_id, a_kicker_id, a_extra_point_made, a_extra_point_attempt, a_field_goal_made, a_field_goal_attempt))
    while cursor.nextset():
        pass
    cursor.close()

# Receives database connection and the data for an existing kicker stat (kicker stat id, extra points made, extra points attempted, field goals made, field goals attempted).
# Updates that kicker stat in the database by calling the sp_UpdateKickerStat stored procedure with
def update_kicker_stats_query(db, u_kicker_stat_id, u_extra_point_made, u_extra_point_attempt, u_field_goal_made, u_field_goal_attempt): 

    # Using parameterized queries (Prevents SQL injection attacks) Call on the sp_DeleteKickerStat
    query = "CALL sp_UpdateKickerStat(%s, %s, %s, %s, %s)"
    cursor = db_module.query(dbConnection=db, query=query, query_params=(u_kicker_stat_id, u_extra_point_made,
                            u_extra_point_attempt, u_field_goal_made, u_field_goal_attempt))
    while cursor.nextset():
        pass
    cursor.close()

# Receives database connection and a kicker stat id. 
# Deletes that kicker stat from the database by calling the sp_DeleteKickerStat stored procedure
def delete_kicker_stats_query(db, kicker_stat_id): # DB Connection and stat_id passed from app.py
    kicker_stat_id = int(kicker_stat_id)

    # Using parameterized queries (Prevents SQL injection attacks) Call on the sp_DeleteKickerStat
    query = "CALL sp_DeleteKickerStat(%s)"
    cursor = db_module.query(dbConnection=db, query=query, query_params=(kicker_stat_id,))
    while cursor.nextset():
        pass
    cursor.close()

