# File name: conference_division.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains the database query function for getting teams by conference and division.
#       Imported and used in app.py to retrieve the data to render the data in teams.j2 template

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology)and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection and conference name (either "AFC", "NFC", or "All").
# Returns list of teams in that conference along with their home city, conference, and division
def get_teams_by_conference(db, conference):
    if conference == "All":
        query =  """
            SELECT t.team_name AS Team, t.team_home AS Home, cd.conference AS Conference, cd.division AS Division
            FROM Teams as t
                INNER JOIN ConferenceDivisions as cd 
                    ON t.conference_division_id = cd.conference_division_id
            ORDER BY t.team_name;"""
        teams = db_module.query(dbConnection=db, query=query).fetchall()
    else:
        query =  """
            SELECT t.team_name AS Team, t.team_home AS Home, cd.conference AS Conference, cd.division AS Division
            FROM Teams as t
                INNER JOIN ConferenceDivisions as cd 
                    ON t.conference_division_id = cd.conference_division_id
            WHERE cd.conference = %s
            ORDER BY t.team_name;"""
        teams = db_module.query(dbConnection=db, query=query, query_params=(conference, )).fetchall()
    return teams