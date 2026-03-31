# File name: app.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: is the main Flask application file for the project. 
#       It defines the different routes and handlers for the web application, connects to the database, 
#       and renders the appropriate templates with the data retrieved from the database. 
#       It also handles form submissions for creating, updating, and deleting records in the database. 
#       The app.py file imports various query functions from the database/queries directory to interact with the database 
#       and perform the necessary CRUD operations based on user interactions with the web application.

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
import database.db_connector as db
import os
import MySQLdb

#importing the different queries
from database.queries.conference_division import get_teams_by_conference
from database.queries.teams import get_teams_data, get_list_of_teams
from database.queries.players import get_players_data
from database.queries.games import get_games_data, delete_game_query, get_player_games, create_game_query
from database.queries.offensive_stats import get_offensive_stats
from database.queries.kicker_stats import *
from database.queries.defensive_stats import get_defensive_stats
from database.queries.reset import reset_db

PORT = 59387

app = Flask(__name__)
app.secret_key = "dev"

#-----------------------------------------------------------------
# Home Handler
#-----------------------------------------------------------------
# READ Route for home page to render the home.j2 template
@app.route("/", methods=["GET"])
def home():
    # Render the home.j2 template when the user navigates to the home page
    try:
        return render_template("home.j2")

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500

#-----------------------------------------------------------------
# Conference and Division Handler
#-----------------------------------------------------------------
# READ Route for conference and division page to render the conference_division.j2 template and pass in the teams based on the user-selected conference/division
@app.route("/cd", methods=["GET", "POST"])
def retrieve_conferenceDivision():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select "All" conferences/divisions and pass to the conference_division.j2 template to render the teams table
        default_conference = "All"
        teams_list = get_teams_by_conference(dbConnection, default_conference)

        # Change the selection once a selection is made by the user in the dropdown form in the conference_division.j2 template and the form is submitted
        if request.method == "POST":
            selected_conference = request.form.get("conference", "All")
            teams_list = get_teams_by_conference(dbConnection, selected_conference)

        # Pass the teams_list to the conference_division.j2 template to render the teams table, either the default list of all teams or the user selected conference
        return render_template("conference_division.j2", j2_teams=teams_list)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# Defensive Stats Handler
#-----------------------------------------------------------------
# READ Route for defensive stats page to render the defensive_stats.j2 template and pass in the defensive stats data retrieved from the DB
@app.route("/defensive-stats", methods=["GET"])
def retrieve_defensive_stats():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all defensive stats and pass to the defensive_stats.j2 template to render the defensive stats table
        defensive_stats = []
        defensive_stats = get_defensive_stats(dbConnection)
        return render_template("defensive_stats.j2", j2_defensive_stats=defensive_stats)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# Games Handlers
#-----------------------------------------------------------------
# READ route for games page to retrieve all games from the DB and render the games.j2 template
@app.route("/games", methods=["GET"])
def retrieve_game():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all games and pass to the games.j2 template to render the games table
        games = []
        games = get_games_data(dbConnection)

        # Get list of teams for the add game form select options in the games.j2 template
        team_list = []
        team_list = get_list_of_teams(dbConnection)
        return render_template("games.j2", j2_games=games, j2_teams=team_list)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

# CREATE route for games page to add new game to the DB based on user input from the form in games.j2 template
@app.route("/games/add", methods=["POST"])
def add_game_route():
    try:
        # Open DB connection
        dbConnection = db.connectDB()
    
        # Recieve data from jinja add form in the games page and validate submissions to prevent data discrepencies
        # If the data is not valid, flash an error message and redirect the user back to the games page
        try:
            a_home_team_id = int(request.form["home_team_id"])
            a_home_points_scored= int(request.form["home_points_scored"])
            a_away_team_id = int(request.form["away_team_id"])
            a_away_points_scored = int(request.form["away_points_scored"])
            a_week_number = int(request.form["week_number"])
            a_year = int(request.form["year"])
        except (KeyError, ValueError):
            flash("All fields must have a value.")
            return redirect(url_for("retrieve_game"))
        
        # Call imported create_game_query function from the games.py file
        # Pass the DB connection and the cleansed data, if successful flash success message and redirect user back to the games page
        create_game_query(dbConnection, a_home_team_id, a_home_points_scored, a_away_team_id, a_away_points_scored, a_week_number, a_year)
        flash("Game added successfully!")
        return redirect(url_for("retrieve_game"))
    
    # Error handling for duplicate game entry based on unique constraint in the DB. 
    # If a duplicate game is being added, flash an error message and redirect the user back to the games page
    # For any other database errors, print the error and return a generic database error message
    except MySQLdb.Error as e:
        if e.args[0] == 1062:
            flash("ERROR: Cannot have duplicate games.")
            return redirect(url_for("retrieve_game"))
        print(e)
        return "Database error has occurred", 500
    
    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500

    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

# DELETE route for games page to delete a game from the DB based on the game id passed from the jinja form in the games.j2 template
@app.route("/games/delete", methods=["POST"])
def delete_game_route():
    try:
        # Open DB connection
        dbConnection = db.connectDB()
        
        # Retrieve the game id from jinja form and set as game_id. 
        # Pass DB connection and game_id to imported delete_game_query function from the games.py file to delete the game from the DB 
        # Redirect the user back to the games page where the deleted game will no longer be displayed
        game_id = request.form["game_id"]
        delete_game_query(dbConnection, game_id)
        return redirect("/games")

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# Kicker Stats Handlers
#-----------------------------------------------------------------
# READ route for kicker stats page to retrieve all kicker stats from the DB
@app.route("/kicker-stats", methods=["GET"])
def retrieve_kicker_stats():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all kicker stats and pass to the kicker_stats.j2 template to render the kicker stats table
        kicker_stat_list = []
        kicker_stat_list = get_kicker_stats(dbConnection)
        return render_template("kicker_stats.j2", j2_kicker_stats=kicker_stat_list)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

# CREATE route for kicker stats page to add new kicker stats to the DB
@app.route("/kicker-stats/add", methods=["POST"] )
def create_kicker_stats():
    try:
        # Open DB connection
        dbConnection = db.connectDB()
    
        # Recieve user data from jinja add form in the kicker_stats page and validate submissions to prevent data discrepencies
        try:
            a_kicker_id = int(request.form["kicker_id"])
            a_week= int(request.form["week"])
            a_year = int(request.form["year"])
            a_home_team_id = int(request.form["home_team_id"])
            a_away_team_id = int(request.form["away_team_id"])
            a_extra_point_made = int(request.form["extra_point_made"])
            a_extra_point_attempt = int(request.form["extra_point_attempt"])
            a_field_goal_made = int(request.form["field_goal_made"])
            a_field_goal_attempt = int(request.form["field_goal_attempt"])

            # Defensive programming to check if the numbers passed in the form are negative
            for entry in [a_extra_point_made, a_extra_point_attempt, a_field_goal_made, a_field_goal_attempt]:
                if entry < 0:
                    raise ValueError("Stats cannot be negative")

        # Error handling for missing form data or invalid data types
        except (KeyError, ValueError) as e:
            return str(e)
        
        # Call imported create_kicker_stats_query function from the kicker_stats.py file
        # Pass the DB connection and the cleansed data
        create_kicker_stats_query(dbConnection, a_kicker_id, a_week, a_year, a_home_team_id, a_away_team_id, 
                              a_extra_point_made, a_extra_point_attempt, a_field_goal_made, a_field_goal_attempt)
        return redirect("/kicker-stats")
    
    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

# Flask endpoint for AJAX request for stats_kicker add form (could be used for future forms)
@app.route("/kicker-stats/<int:player_id>", methods=["GET"])
def create_sub_player_games(player_id):
    try:
        # Open DB connection
        dbConnection = db.connectDB()
        
        # Query the DB for games this player has played
        games = get_player_games(dbConnection, player_id)
        # Return JSON to JS
        return jsonify([dict(g) for g in games])
    
    except Exception as e:
        print(f"Error processing AJAX request: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

# UPDATE route for kicker stats page to update existing kicker stats in the DB
# Will reroute user to a new page with a form pre-populated with the existing kicker stats data based on the stat id passed in the URL
@app.route("/kicker-stats/<int:id>/edit", methods=["GET", "POST"])
def update_kicker_stats(id):
    
    # If the user is navigating to the edit page, render the edit page with the existing data pre-populated in the form
    if request.method == "GET":
        try:
            # Open DB connection
            dbConnection = db.connectDB()

            # Retrieve the kicker stats data based on the passed id from the DB and pass the data to the edit page to pre-populate the form with the existing data
            kicker_stats_list = []
            kicker_stats_list = get_kicker_stats_for_update(dbConnection, id)
            return render_template("kicker_stats_edit.j2", j2_kicker_stats=kicker_stats_list)

        except Exception as e:
            print(f"Error rendering page: {e}")
            return "An error occurred while rendering the page.", 500
        
        finally:
            if  "dbConnection" in locals() and dbConnection:
                dbConnection.close()

    if request.method == "POST":
        try:
            # Open DB connection
            dbConnection = db.connectDB()

            # Get the kicker stat id to update from jinja form in the kicker_stats_edit page
            u_kicker_stat_id = int(request.form["kicker_stat_id"])
            
            # Cleanse data - If numbers are not passed in the form change the values to 0
            try:
                u_extra_point_made = int(request.form["extra_point_made"])
            except ValueError:
                u_extra_point_made = 0
            try:
                u_extra_point_attempt = int(request.form["extra_point_attempt"])
            except ValueError:
                u_extra_point_attempt = 0
            try:
                u_field_goal_made = int(request.form["field_goal_made"])
            except ValueError:
                u_field_goal_made = 0
            try:
                u_field_goal_attempt = int(request.form["field_goal_attempt"])
            except ValueError:
                u_field_goal_attempt = 0

            # Call imported update_kicker_stats_query function from the kicker_stats.py file
            # Pass the DB connection and the cleansed data
            update_kicker_stats_query(dbConnection, u_kicker_stat_id, u_extra_point_made, u_extra_point_attempt, u_field_goal_made, u_field_goal_attempt)

            # Redirect the user to the updated webpage. The updated kicker stat will be reflected in the kicker stats table on the webpage based on the passed id
            return redirect("/kicker-stats")

        except Exception as e:
            print(f"Error rendering page: {e}")
            return "An error occurred while executing the database queries.", 500

        finally:
            if  "dbConnection" in locals() and dbConnection:
                dbConnection.close()


@app.route("/kicker-stats/delete", methods=["POST"] )
def delete_kicker_stats():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # Retrieve the kicker_stats_id from jinja form and set as stat_id
        stat_id = request.form["kicker_stats_id"]

        # Call imported delete_kicker_stats_query function from the kicker_stats.py file
        # Pass the DB connection and the stat_id
        delete_kicker_stats_query(dbConnection, stat_id)

        # Redirect the user to the updated webpage
        return redirect("/kicker-stats")

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
            dbConnection.close()

#-----------------------------------------------------------------
# Offensive Stats Handler
#-----------------------------------------------------------------
@app.route("/offensive-stats", methods=["GET"])
def retrieve_offensive_stats():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all offensive stats and pass to the offensive_stats.j2 template to render the offensive stats table
        offensivestats = []
        offensivestats = get_offensive_stats(dbConnection)
        return render_template("offensive_stats.j2", j2_offensivestats=offensivestats)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# Players Handler
#-----------------------------------------------------------------
@app.route("/players", methods=["GET"])
def retrieve_players():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all players and pass to the players.j2 template to render the players table
        list_players = []
        list_players = get_players_data(dbConnection)
        return render_template("players.j2", j2_players=list_players)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# Teams Handler
#-----------------------------------------------------------------
@app.route("/teams", methods=["GET"])
def retrieve_teams():
    try:
        # Open DB connection
        dbConnection = db.connectDB()

        # By default, select all teams and pass to the teams.j2 template to render the teams table
        teams_list = []
        teams_list = get_teams_data(dbConnection)
        return render_template("teams.j2", j2_teams=teams_list)

    except Exception as e:
        print(f"Error rendering page: {e}")
        return "An error occurred while rendering the page.", 500
    
    finally:
        if  "dbConnection" in locals() and dbConnection:
             dbConnection.close()

#-----------------------------------------------------------------
# reset_db Handler
#-----------------------------------------------------------------
# This route will reset the database to its initial state by running the DDL.sql file
# This can be used for testing purposes to reset the DB after performing CRUD operations
@app.route("/reset", methods=["POST"])
def reset_route():
    # Get the next URL to redirect to after resetting the database, default to home page if not provided
    # This allows us to reuse the reset button on multiple pages and redirect the user back to the page they were on after resetting the database
    next_url = request.form.get("next", "/")
    if not next_url.startswith("/"):
        next_url = "/"
    
    # Define the path to the DDL.sql file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DDL_PATH = os.path.join(BASE_DIR, "..", "DDL.sql")

    # Try to reset the database by running the DDL.sql file
    # If successful, redirect the user to the next_url
    # If there is an error, print the error and return a generic error message
    dbConnection = None
    try:
        dbConnection = db.connectDB()
        # run DDL.sql 
        reset_db(dbConnection, DDL_PATH)
        # run routines ??
        return redirect(next_url)

    except Exception as e:
        print(f"Error resetting database: {e}")
        return "Reset failed.", 500

    finally:
        if dbConnection:
            dbConnection.close()

#-----------------------------------------------------------------
# Listener to run the Flask application
#-----------------------------------------------------------------
# Run the Flask application on the specified port with debug mode enabled
# Debug is an optional parameter. Behaves like nodemon in Node, automatically restarting the server when it detects changes to files in the directory
if __name__ == "__main__":
    app.run(
        port=PORT, debug=True
    )