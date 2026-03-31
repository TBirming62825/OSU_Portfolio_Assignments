CS 340 Group 110
Group Project
Authors: Timothy Birmingham and Cory Hungate

General Code Citations:
    The code in this repo was primarily based on the example python and .j2 code provided in the Week 6 (Exploration: web application technology)
    and Week 8 (exploration: implementing CUD in your app) explorations for this class. 
    The modifications to those files found throughout this repo represent original work by the authors

Setup Instructions

This project uses Python, Flask, and MariaDB. Follow the steps below to run the application either locally or on the OSU servers.
Please note that if running the file locally, a local mariadb will need to be installed. Doing so is outside the scope of the document
but many tutorials are available online.

1. Clone the Repository
    git clone https://github.com/TBirming62825/CS_340_Group_110.git
    cd final_project_site

2. Create a Virtual Environment
    Create a virtual environment to isolate project dependencies.
        python3 -m venv venv

3. Activate the Virtual Environment

    Mac/Linux:
        source venv/bin/activate

    Windows:
        venv\Scripts\activate

    Once activated, your terminal should show (venv).

4. Install Required Libraries
    Install all dependencies using the provided requirements.txt file.
        pip install -r requirements.txt

    This will install:
        Flask, mysqlclient, python-dotenv

5. Configure Environment Variables

    Create a .env file in the project root directory. 
    Note that an example .env.example has been proveded in the repo

    Example:
        DB_HOST=localhost
        DB_USER=your_username
        DB_PASSWORD=your_password
        DB_NAME=your_database
        DB_PORT=3306

    Note that the variables inside db_connector are already set to accept these environment variables

6. Run the Application
    Start the Flask application with:
        python3 app.py

The application will start a local development server.

7. Open in Browser
    Navigate to:
        http://127.0.0.1:<your_port_number>
    to view the application.

Testing Procedure

1. Navigate to the "Games" page.
2. In the Add Games section, select "Ravens" for either the home or away team in the drop down. Then select one of the remaining teams for the other option (remember your selection).
3. (CREATE) Add points scored, week number, and year data. Then click "Add Game" under the "Actions" column on the far right. (Your game will now appear in the Games table below!)
4. Navigate to the "Kicker Stats" page.
5. In the Add Kicker Stat secrtion, select the kicker for the team that you selected in part 2 (not the "Ravens")
4. The grayed out drop downs will now become selectable. Select the week number and year you entered in part 3 (will be the only options available in the drop downs).
5. (CREATE) Add extra points made, extra point attempts, field goals made, and field goal attempts data. Then click "Add Kicker Stat" under the "Actions" column on the far right. (Your kicker stat will now appear in the kicker stats table below!)
6. Now try selecting the "Update" botton under the "Actions" column on the far right of the kicker stats table for the new kicker stat your created. This will navigate you to the edit kicker stats page.
7. (UPDATE) Make some changes to your new kicker stat and hit "Save" on the far right. This will take you back to the kicker stats page. (Your edits will will now appear in the kicker stats table below!)
8. (DELETE) Now try selecting "Delete" on the far right under the "Actions" column for the new kicker stat you created/updated. (Your kicker stat will now be removed from the kicker stat table!)
9. Now navigate back to the "Games" page. 
10. (DELETE) Now try selecting "Delete" on the far right under the "Actions" column for the "Ravens" game you created. (Your game will now be removed from the games table!)
Note: Steps 8-10 can also performed by selecting the "Reset DB" button located in the navigation bar. This button will reset the database back to its original data and remove the newly created/updated game and stat.
