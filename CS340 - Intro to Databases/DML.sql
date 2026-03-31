-- file: DML.sql
-- Authors: Timothy Birmingham and Cory Hungate
-- This file contains the data definition queries for the final project for team 110 for the class CS 340

-- CREATE (INSERT) statements found in
    -- Games and StatsKicker
-- RETRIEVE (SELECT) statements found in 
    -- ConferenceDivisions, Teams, Players, Games, StatsKicker, StatsOffensive, StatsDefensive
-- UPDATE statement found in
    -- StatsKicker
-- DELETE statement found in
    -- Games and StatsKicker

-- The queries on this page represent original work by the authors


-- ===================================================
-- ConferenceDivisions Queries
-- ===================================================
-- Query to retrieve teams along with their home city, conference, and division
SELECT t.team_name AS Team, t.team_home AS Home, cd.conference AS Conference, cd.division AS Division
FROM Teams as t
INNER JOIN ConferenceDivisions as cd 
    ON t.conference_division_id = cd.conference_division_id
ORDER BY t.team_name;

-- Query to return teams along with their home city, conference, and division in the NFC 
-- (website has functionality to select which conference you want to see information about. This is just a sample where the user selects NFC)
SELECT t.team_name AS Team, t.team_home AS Home, cd.conference AS Conference, cd.division AS Division
FROM Teams as t
INNER JOIN ConferenceDivisions as cd 
    ON t.conference_division_id = cd.conference_division_id
WHERE cd.conference = 'NFC'
ORDER BY t.team_name;


-- ===================================================
-- StatsDefensive Queries
-- ===================================================
-- Query to return defensive stats for all teams and their opponents
-- Need to use a UNION ALL to combine the results for home and away games, 
-- since opponent team is stored in different columns in the Games table depending on whether the team is playing at home or away
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


-- ===================================================
-- Games Queries
-- ===================================================
-- Query to return games data, including home team, away team, points scored, week number, year, and game id
SELECT  t_home.team_name AS home_team,
    Games.home_points_scored,
    t_away.team_name AS away_team,
    Games.away_points_scored,
    Games.week_number,
    Games.year,
    Games.game_id
FROM Games
JOIN Teams t_home
    ON Games.home_team_id = t_home.team_id
JOIN Teams t_away
    ON Games.away_team_id = t_away.team_id

-- Query to return a sepcified kicker's games, includes  home team, away team, week number, year, and game id. 
-- Only returns games for players in the kicker position who do not have stats recorded for that game in the StatsKicker table
-- (website has functionality to select which kicker you want to see information about. This is just a sample where the user selects Brandon Aubrey with player_id =18)
SELECT 
    g.game_id,
    g.week_number,
    g.year,
    t_a.team_name AS away_team,
    t_a.team_id As away_team_id,
    t_h.team_name AS home_team,
    t_h.team_id As home_team_id
FROM Games AS g
INNER JOIN Teams AS t_a
    ON g.away_team_id = t_a.team_id
INNER JOIN Teams AS t_h
    ON g.home_team_id = t_h.team_id
INNER JOIN Players AS p
    ON p.player_id = 18
WHERE p.position = 'K'
    AND (p.team_id = g.home_team_id OR p.team_id = g.away_team_id)
    AND NOT EXISTS (
        SELECT 1
        FROM StatsKicker as sk
        WHERE sk.game_id = g.game_id AND sk.player_id = 18)
ORDER BY g.year, g.week_number;

-- Query to insert a new row into the Games table
-- (website has functionality to specifiy the specific data for the game. This is just a sample where the user selects 
-- home_team_id = 1, home_points_scored = 14, away_team_id = 4, away_points_scored = 24, week_number = 8, year = 2026) 
INSERT INTO Games (`home_team_id`, `home_points_scored`, `away_team_id`, `away_points_scored`, `week_number`, `year`) 
VALUES (1, 14, 4, 24, 8, 2026);

-- Query to remove a specified row in the Games table
-- (website has functionality to specifiy the specific game. This is just a sample where the user selects game_id = 2)
DELETE FROM Games 
WHERE game_id = 2;


-- ===================================================
-- StatsKicker Queries
-- ===================================================
-- Query to return kicker stats for all teams and their opponents
-- Need to use a UNION ALL to combine the results for home and away games, since opponent team is stored 
-- in different columns in the Games table depending on whether the team is playing at home or away
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

-- Query to return specified kicker stat's data, including player name, team, opponent, extra points made/attempted, and field goals made/attempted
-- (website has functionality to select which kicker stat you want to see information about to later update.
-- This is just a sample where the user selects the kicker stat with kicker_stat_id = 1)
SELECT sk.kicker_stats_id,
    CONCAT(p.first_name, " ", p.last_name) as name, 
    home.team_name as team, 
    away.team_name as opponent, 
    sk.extra_point_made,
    sk.extra_point_attempt, 
    sk.field_goal_made, 
    sk.field_goal_attempt, 
    sk.kicker_stats_id
FROM Players as p
INNER JOIN StatsKicker as sk 
    ON p.player_id = sk.player_id
INNER JOIN Games as g
    ON sk.game_id = g.game_id
INNER JOIN  Teams as home
    ON g.home_team_id = home.team_id
INNER JOIN Teams as away
    ON g.away_team_id = away.team_id
WHERE sk.kicker_stats_id = 1

-- Query to return a game_id based on a sepcified home_team_id, away_team_id, week_number, and year
-- (website has functionality to select which game_id you want to see information about. 
-- This is just a sample where the user selects home_team_id = 1, away_team_id = 3, week_number = 9, and year = 2025)
SELECT game_id 
FROM Games 
WHERE home_team_id = 1 AND away_team_id = 3 AND week_number = 9 AND year = 2025

-- Query to return a team_id based on a sepcified player_id
-- (website has functionality to select which team_id you want to see information about. 
-- This is just a sample where the user selects Brandon Aubrey with player_id =18)
SELECT team_id
FROM Players
WHERE player_id = 18

-- Query to insert a new row into the StatsKicker table
-- (website has functionality to specifiy the specific data for the kicker stat. This is just a sample where the user selects 
-- game_id = 2, team_id = 1, player_id = 18, extra_point_made = 3, extra_point_attempt = 4, field_goal_made = 3, field_goal_attempt = 3)
-- ********** NOTE: The below query should be run AFTER running the query to insert a new row into the Games table. 
-- ********** This is because the DDL is designed to not allow for duplicate stat entries for the same player in the same game. 
-- ********** So we need to create a new game for that player first before insterting data.
INSERT INTO StatsKicker (game_id, team_id, player_id, extra_point_made, extra_point_attempt, field_goal_made, field_goal_attempt) 
VALUES (4, 1, 18, 3, 4, 3, 3);

-- Query to update an existing row into the StatsKicker table
-- (website has functionality to specifiy the specific data and kicker for the kicker stat. This is just a sample where the user selects 
-- extra_point_made = 5, extra_point_attempt = 6, field_goal_made = 3, field_goal_attempt = 3, and kicker_stats_id = 1)
UPDATE StatsKicker SET extra_point_made = 5, 
                       extra_point_attempt = 6,
                       field_goal_made = 3,
                       field_goal_attempt = 3
                    WHERE kicker_stats_id = 1; 

-- Query to remove a specified row in the StatsKicker table
-- (website has functionality to specifiy the specific kciker stat. This is just a sample where the user selects kicker_stats_id = 1)
DELETE FROM StatsKicker WHERE kicker_stats_id = 1;


-- ===================================================
-- StatsOffensive Queries
-- ===================================================
-- Query to return offensive stats for all teams and their opponents
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

-- ===================================================
-- Players Queries
-- ===================================================
-- Query to return players data for all teams, including player name, team name, and position
SELECT CONCAT(Players.first_name, " ", Players.last_name) as Name, Teams.team_name AS Team, Players.position AS Position
FROM Players
LEFT JOIN Teams
    ON Players.team_id = Teams.team_id
ORDER BY Team, Position DESC;


-- ===================================================
-- Teams Queries
-- ===================================================
-- Query to return teams data for all teams, including team name, home city, and player count
SELECT Teams.team_name, Teams.team_home, COUNT(Players.player_id) as player_count
FROM Teams
LEFT JOIN Players 
    ON Teams.team_id = Players.team_id
GROUP BY Teams.team_id
ORDER BY Teams.team_id;

-- Query to return team names and team ids for all teams, ordered alphabetically by team name
SELECT team_id, team_name 
FROM Teams
ORDER BY team_name;