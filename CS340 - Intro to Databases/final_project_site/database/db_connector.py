# File name: db_connector.py 

# Authors: Timothy Birmingham and Cory Hungate

# Description: Contains functions to connect to the database and execute queries on the database.
# Imported and used in all the query files in the database/queries directory to connect to the database and execute queries on the database.

# Code Citations: The code in this file is nearly identical to the example connector file provided in the Week 6 
#       example code. Minor modification to allow the use of .env variables. These modifications to that code 
#       represent original work by the authors

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

# Database credentials
host = os.getenv("DB_HOST")   
user = os.getenv("DB_USER")       
passwd = os.getenv("DB_PASSWORD")     
db = os.getenv("DB_NAME") 

# Function to connect to the database and return a database connection object
def connectDB(host = host, user = user, passwd = passwd, db = db):
    '''
    connects to a database and returns a database object
    '''
    dbConnection = MySQLdb.connect(host,user,passwd,db)
    return dbConnection

# Function to execute a given SQL query on the given database connection and return a cursor object
def query(dbConnection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object
    dbConnection: a MySQLdb connection object created by connectDB()
    query: string containing SQL query
    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.
    '''

    if dbConnection is None:
        print("No connection to the database found! Have you called connectDB() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params));
    # Create a cursor to execute query. Why? Because they optimize execution by retaining a reference according to PEP0249
    cursor = dbConnection.cursor(MySQLdb.cursors.DictCursor)

    # Sanitize the query before executing it.
    cursor.execute(query, query_params)
    
    # Commit any changes to the database.
    dbConnection.commit()
    
    return cursor