-- file: PL.sql
-- Authors: Timothy Birmingham and Cory Hungate
-- this file contains the prodecure logic for the final project for team 110
-- for the class CS 340

-- code citation
-- these procedures are modified from the code provided in the week 8 exploration: 
-- implementing CRUD operations in your app. 


-- #############################
-- CREATE Games row
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateGame;

DELIMITER //
CREATE PROCEDURE sp_CreateGame(
    IN p_home_team_id INT, 
    IN p_home_points_scored INT,
    IN p_away_team_id INT,
    IN p_away_points_scored INT,
    IN p_week_number INT,
    IN p_year INT
    )

BEGIN
    INSERT INTO Games (`home_team_id`,
                `home_points_scored`,
                `away_team_id`,
                `away_points_scored`,
                `week_number`,
                `year`) 
    VALUES (p_home_team_id,
            p_home_points_scored,
            p_away_team_id,
            p_away_points_scored,
            p_week_number,
            p_year);
END //
DELIMITER ;

-- ##############################
-- DELETE Games row
-- ##############################
DROP PROCEDURE IF EXISTS sp_DeleteGame;
DELIMITER //
CREATE PROCEDURE sp_DeleteGame(IN gid INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on any error
        ROLLBACK;
        -- Propogate the custom error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;
        -- Deleting corresponding row from Games table
        -- Will also remove the game from all stats tables
        DELETE FROM Games WHERE game_id = gid;
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Games for id: ', gid);
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- CREATE statskicker row
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateKickerStat;

DELIMITER //
CREATE PROCEDURE sp_CreateKickerStat(
    IN p_game_id INT, 
    IN p_team_id INT,
    IN p_player_id INT,
    IN p_extra_point_made INT,
    IN p_extra_point_attempt INT,
    IN p_field_goal_made INT,
    IN p_field_goal_attempt INT
    )

BEGIN
    INSERT INTO StatsKicker (game_id, 
                            team_id, 
                            player_id, 
                            extra_point_made, 
                            extra_point_attempt, 
                            field_goal_made, 
                            field_goal_attempt) 
            VALUES (p_game_id, 
                    p_team_id, 
                    p_player_id, 
                    p_extra_point_made, 
                    p_extra_point_attempt, 
                    p_field_goal_made, 
                    p_field_goal_attempt);
END //
DELIMITER ;


-- #############################
-- UPDATE statskicker row
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateKickerStat;

DELIMITER //
CREATE PROCEDURE sp_UpdateKickerStat(IN p_kicker_stat_id INT,
                                    IN p_extra_point_made INT,
                                    IN p_extra_point_attempt INT,
                                    IN p_field_goal_made INT,
                                    IN p_field_goal_attempt INT)
BEGIN
    UPDATE StatsKicker SET extra_point_made = p_extra_point_made,
                        extra_point_attempt = p_extra_point_attempt,
                        field_goal_made = p_field_goal_made,
                        field_goal_attempt = p_field_goal_attempt
                        WHERE kicker_stats_id = p_kicker_stat_id; 
END //
DELIMITER ;


-- ##############################
-- DELETE statskicker row
-- ##############################
DROP PROCEDURE IF EXISTS sp_DeleteKickerStat;
DELIMITER //
CREATE PROCEDURE sp_DeleteKickerStat(IN p_kicker_stats_id INT)
BEGIN
    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;
        -- Deleting corresponding row from statskicker table
        DELETE FROM StatsKicker WHERE kicker_stats_id = p_kicker_stats_id;
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in StatsKicker for id: ', p_kicker_stats_id);
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

