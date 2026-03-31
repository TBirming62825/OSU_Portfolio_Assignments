# File name: reset.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains function to reset database by executing all the queries in DDL.sql.
#       Imported and used in app.py when user clicks "Reset Database" button on home page

# Code Citations: The code in this file was primarily based on the example python provided in the Week 6 
#       (Exploration: web application technology) and Week 8 (exploration: implementing CUD in your app) explorations for this class
#       All modifications to that code represent original work by the authors

import database.db_connector as db_module

# Receives database connection and filepath to DDL.sql file. 
# Executes all the queries in DDL.sql to reset the database to its initial state.
# Note: DDL.sql contained in the directory above final_project_site
def reset_db(db, filepath):
    
    # Read the DDL.sql file and split it into individual queries by the ";" delimiter
    with open(filepath, "r") as f:
        ddl = f.read()    
    queries = ddl.split(";")

    # Execute each query in the DDL.sql file to reset the database. 
    # Strip any whitespace from the query and check if it's not empty before executing
    for query in queries:
        query = query.strip()
        if query:
            db_module.query(dbConnection=db, query=query)

    # Commit the changes to the database after executing all the queries
    db.commit()