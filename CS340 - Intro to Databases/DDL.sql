-- file: DDL.sql
-- Authors: Timothy Birmingham and Cory Hungate
-- this file contains the data definition queries for the final project for team 110
-- for the class CS 340

--  the following CREATE TABLE statements were made with MySQL Workbench 
--  Forward Engineering based on our defined schema and minor changes made by the authors
--  Insert statements are original creations of group members

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP TABLE IF EXISTS ConferenceDivisions, Teams, Players, Games, StatsKicker, StatsOffensive, StatsDefensive; 

-- -----------------------------------------------------
-- Table `ConferenceDivision`
-- -----------------------------------------------------
CREATE TABLE `ConferenceDivisions` (
  `conference_division_id` INT NOT NULL AUTO_INCREMENT,
  `conference` VARCHAR(3) NOT NULL,
  `division` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`conference_division_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Teams`
-- -----------------------------------------------------
CREATE TABLE `Teams` (
  `team_id` INT NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(145) NOT NULL,
  `team_home` VARCHAR(145) NOT NULL,
  `conference_division_id` INT NOT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE INDEX `idTeams_UNIQUE` (`team_id` ASC) VISIBLE,
  INDEX `fk_Teams_ConferenceDivision1_idx` (`conference_division_id` ASC) VISIBLE,
  CONSTRAINT `fk_Teams_ConferenceDivision1`
    FOREIGN KEY (`conference_division_id`)
    REFERENCES `ConferenceDivisions` (`conference_division_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Players`
-- -----------------------------------------------------
CREATE TABLE `Players` (
  `player_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(145) NOT NULL,
  `last_name` VARCHAR(145) NOT NULL,
  `position` VARCHAR(45) NOT NULL,
  `team_id` INT NOT NULL,
  PRIMARY KEY (`player_id`),
  INDEX `player_team_idx` (`team_id` ASC) VISIBLE,
  CONSTRAINT `player_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Games`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE `Games` (
  `game_id` INT NOT NULL AUTO_INCREMENT,
  `home_team_id` INT NOT NULL,
  `away_team_id` INT NOT NULL,
  `home_points_scored` INT UNSIGNED NOT NULL,
  `away_points_scored` INT UNSIGNED NOT NULL,
  `week_number` INT UNSIGNED NOT NULL,
  `year` YEAR(4) NOT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE INDEX `idgame_UNIQUE` (`game_id` ASC) VISIBLE,
  UNIQUE KEY (`home_team_id`, `away_team_id`, `week_number`),
  INDEX `home_idteam_idx` (`home_team_id` ASC) VISIBLE,
  INDEX `away_idteam_idx` (`away_team_id` ASC) VISIBLE,
  CONSTRAINT `home_idteam`
    FOREIGN KEY (`home_team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `away_idteam`
    FOREIGN KEY (`away_team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `StatsKicker`
-- -----------------------------------------------------
CREATE TABLE `StatsKicker` (
  `kicker_stats_id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `player_id` INT NOT NULL,
  `extra_point_made` INT UNSIGNED NULL,
  `extra_point_attempt` INT UNSIGNED NULL,
  `field_goal_made` INT UNSIGNED NULL,
  `field_goal_attempt` INT UNSIGNED NULL,
  PRIMARY KEY (`kicker_stats_id`),
  INDEX `kicker_idplayer_idx` (`player_id` ASC) VISIBLE,
  INDEX `kicker_idteam_idx` (`team_id` ASC) VISIBLE,
  INDEX `kicker_idgame_idx` (`game_id` ASC) VISIBLE,
  UNIQUE KEY (`player_id`, `game_id`),
  CONSTRAINT `kicker_idplayer`
    FOREIGN KEY (`player_id`)
    REFERENCES `Players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kicker_idteam`
    FOREIGN KEY (`team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `kicker_idgame`
    FOREIGN KEY (`game_id`)
    REFERENCES `Games` (`game_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `StatsOffensive`
-- -----------------------------------------------------
CREATE TABLE `StatsOffensive` (
  `offensive_stats_id` INT NOT NULL AUTO_INCREMENT,
  `player_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `pass_attempt` INT UNSIGNED NULL,
  `pass_complete` INT UNSIGNED NULL,
  `pass_yards` INT NULL,
  `pass_touchdown` INT UNSIGNED NULL,
  `pass_interception` INT UNSIGNED NULL,
  `rush_attempt` INT UNSIGNED NULL,
  `rush_yard` INT NULL,
  `rush_touchdown` INT UNSIGNED NULL,
  `receiving_target` INT UNSIGNED NULL,
  `receiving_reception` INT UNSIGNED NULL,
  `receiving_yard` INT NULL,
  `receiving_touchdown` INT UNSIGNED NULL,
  `two_point_conversion` INT UNSIGNED NULL,
  `fumble` INT UNSIGNED NULL,
  PRIMARY KEY (`offensive_stats_id`),
  INDEX `offense_idteam_idx` (`team_id` ASC) VISIBLE,
  INDEX `offense_id_player_idx` (`player_id` ASC) VISIBLE,
  INDEX `offense_idgame_idx` (`game_id` ASC) VISIBLE,
  UNIQUE KEY (`player_id`, `game_id`),
  CONSTRAINT `offense_id_player`
    FOREIGN KEY (`player_id`)
    REFERENCES `Players` (`player_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `offense_idteam`
    FOREIGN KEY (`team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `offense_idgame`
    FOREIGN KEY (`game_id`)
    REFERENCES `Games` (`game_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `StatsDefensive`
-- -----------------------------------------------------
CREATE TABLE `StatsDefensive` (
  `defensive_stats_id` INT NOT NULL AUTO_INCREMENT,
  `game_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  `defensive_touchdown` INT UNSIGNED NOT NULL,
  `defensive_interception` INT UNSIGNED NOT NULL,
  `fumble_recover` INT UNSIGNED NOT NULL,
  `sack` INT UNSIGNED NOT NULL,
  `safety` INT UNSIGNED NOT NULL,
  `blocked_punt` INT UNSIGNED NOT NULL,
  `points_allowed` INT UNSIGNED NOT NULL,
  `yards_allowed` INT NOT NULL,
  PRIMARY KEY (`defensive_stats_id`),
  INDEX `defense_idgame_idx` (`game_id` ASC) VISIBLE,
  INDEX `defense_idteam_idx` (`team_id` ASC) VISIBLE,
  CONSTRAINT `defense_idgame`
    FOREIGN KEY (`game_id`)
    REFERENCES `Games` (`game_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `defense_idteam`
    FOREIGN KEY (`team_id`)
    REFERENCES `Teams` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Data Insertion
-- -----------------------------------------------------

-- Insert data into ConferenceDivision table
INSERT INTO ConferenceDivisions (conference, division)
VALUES  ('NFC', 'North'),
  ('NFC', 'South'),
  ('NFC', 'East'),
  ('NFC', 'West'),
  ('AFC', 'North'),
  ('AFC', 'South'),
  ('AFC', 'East'),
  ('AFC', 'West');

-- Insert data into teams table
INSERT INTO Teams (team_name, team_home, conference_division_id)
  SELECT 'Cowboys','Dallas', conference_division_id FROM ConferenceDivisions WHERE conference = 'NFC' AND division = 'East'
  UNION
  SELECT 'Panthers','Carolina', conference_division_id FROM ConferenceDivisions WHERE conference = 'NFC' AND division = 'South'
  UNION
  SELECT 'Cardinals','Arizona', conference_division_id FROM ConferenceDivisions WHERE conference = 'NFC' AND division = 'West'
  UNION
  SELECT 'Ravens','Baltimore', conference_division_id FROM ConferenceDivisions WHERE conference = 'AFC' AND division = 'North';

-- Insert data into players table
INSERT INTO Players (first_name, last_name, position, team_id)
  SELECT 'Jacoby', 'Brissett', 'QB', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'Emari', 'Demercado', 'RB', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'Marvin', 'Harrison', 'WR', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'Trey',	'McBride', 'TE', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'James', 'Conner', 'RB', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'Bryce', 'Young', 'QB', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Rico',	'Dowdle', 'RB', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Tetairoa', 'McMillan', 'WR', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Chuba', 'Hubbard', 'RB', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Tommy', 'Tremble', 'TE', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Jake', 'Ferguson',	'TE', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'CeeDee', 'Lamb',	'WR', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'George', 'Pickens', 'WR', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'Javonte', 'Williams', 'RB', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'Dak', 'Prescott', 'QB', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'Ryan',	'Fitzgerald', 'K', team_id FROM Teams WHERE team_name = 'Panthers'
  UNION
  SELECT 'Chad',	'Ryland', 'K', team_id FROM Teams WHERE team_name = 'Cardinals'
  UNION
  SELECT 'Brandon', 'Aubrey', 'K', team_id FROM Teams WHERE team_name = 'Cowboys'
  UNION
  SELECT 'Kyler', 'Murray', 'QB', team_id FROM Teams WHERE team_name = 'Cardinals';

-- Insert data into Games table
INSERT INTO Games (home_team_id, away_team_id, home_points_scored, away_points_scored, week_number, year)
  SELECT
    (SELECT team_id FROM Teams WHERE team_name = 'Cowboys'), 
    (SELECT team_id FROM Teams WHERE team_name = 'Cardinals'),
    17, 27, 9, 2025  
    UNION
  SELECT
    (SELECT team_id FROM Teams WHERE team_name = 'Panthers'), 
    (SELECT team_id FROM Teams WHERE team_name = 'Cowboys'),
    30, 27, 6, 2025 
    UNION
  SELECT
    (SELECT team_id FROM Teams WHERE team_name = 'Cardinals'), 
    (SELECT team_id FROM Teams WHERE team_name = 'Panthers'),
    7, 22, 2, 2025;

-- Insert data into StatsDefensive table
INSERT INTO StatsDefensive (game_id, team_id, defensive_touchdown, defensive_interception, fumble_recover, sack, safety, blocked_punt, points_allowed, yards_allowed)
  SELECT 
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    1,0,0,5,0,1,27,340
  UNION
  SELECT
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),        
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),        
    0,0,0,0,0,0,27,292
  UNION
  SELECT
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),        
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),        
    1,1,1,3,0,0,22,352
  UNION
  SELECT
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),        
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),        
    0,1,2,5,0,0,17,333
  UNION
  SELECT
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),  
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"), 
    0,1,0,1,0,0,30,410
  UNION
  SELECT
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),  
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),        
    0,1,0,1,0,0,21,293;

-- Insert data into StatsKicker table
INSERT INTO StatsKicker (game_id, team_id, player_id, extra_point_made, extra_point_attempt, field_goal_made, field_goal_attempt)
  SELECT 
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    (SELECT player_id FROM Players WHERE first_name = "Brandon" AND last_name = "Aubrey"),
    2,2,1,2
  UNION
  SELECT 
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
        year = "2025" AND week_number = 9),
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
      (SELECT player_id FROM Players WHERE first_name = "Chad" AND last_name = "Ryland"),
      3,3,2,2
  UNION
  SELECT 
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
        year = "2025" AND week_number = 6),
      (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
      (SELECT player_id FROM Players WHERE first_name = "Ryan" AND last_name = "Fitzgerald"),
      3,3,3,3  
  UNION
  SELECT 
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
        year = "2025" AND week_number = 6),
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
      (SELECT player_id FROM Players WHERE first_name = "Brandon" AND last_name = "Aubrey"),
      3,3,2,2  
  UNION
  SELECT 
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
        year = "2025" AND week_number = 2),
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
      (SELECT player_id FROM Players WHERE first_name = "Chad" AND last_name = "Ryland"),
      3,3,2,2 
  UNION
  SELECT 
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
        year = "2025" AND week_number = 2),
      (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
      (SELECT player_id FROM Players WHERE first_name = "Ryan" AND last_name = "Fitzgerald"),
      1,1,1,1;


-- Insert data into StatsOffensive table
INSERT INTO StatsOffensive (player_id, game_id, team_id, pass_attempt, pass_complete, pass_yards, pass_touchdown, pass_interception, 
                            rush_attempt, rush_yard, rush_touchdown,
                            receiving_reception, receiving_yard, receiving_touchdown, receiving_target,
                            two_point_conversion, fumble)
  SELECT 
    (SELECT player_id FROM Players WHERE first_name = "Jake" AND last_name = "Ferguson"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,0,0,0,5,50,0,7,0,1
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "CeeDee" AND last_name = "Lamb"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,0,0,0,7,85,0,12,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "George" AND last_name = "Pickens"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,0,0,0,6,79,0,9,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Javonte" AND last_name = "Williams"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,15,83,0,1,0,0,1,0,1
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Dak" AND last_name = "Prescott"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    39,24,250,1,1,4,34,0,0,0,0,0,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Jacoby" AND last_name = "Brissett"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    31,21,261,2,0,5,4,1,0,0,0,0,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Emari" AND last_name = "Demercado"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,14,78,0,1,-1,0,1,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Marvin" AND last_name = "Harrison"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,0,0,0,7,96,1,10,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Trey" AND last_name = "McBride"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,0,0,0,5,55,1,9,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "James" AND last_name = "Conner"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Kyler" AND last_name = "Murray"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cowboys") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cardinals") AND 
      year = "2025" AND week_number = 9),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Bryce" AND last_name = "Young"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    25,17,199,3,1,3,5,0,0,0,0,0,0,0
  UNION
  SELECT
      (SELECT player_id FROM Players WHERE first_name = "Rico" AND last_name = "Dowdle"),
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
        year = "2025" AND week_number = 6),
      (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
      0,0,0,0,0,30,183,0,4,56,1,5,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Tetairoa" AND last_name = "McMillan"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    0,0,0,0,0,0,0,0,3,29,2,5,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Chuba" AND last_name = "Hubbard"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Tommy" AND last_name = "Tremble"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    0,0,0,0,0,0,0,0,4,39,0,4,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Jake" AND last_name = "Ferguson"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,0,0,0,3,33,1,3,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "CeeDee" AND last_name = "Lamb"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "George" AND last_name = "Pickens"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,0,0,0,9,168,1,11,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Javonte" AND last_name = "Williams"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    0,0,0,0,0,13,29,0,5,5,0,8,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Dak" AND last_name = "Prescott"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Panthers") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Cowboys") AND 
      year = "2025" AND week_number = 6),
    (SELECT team_id FROM Teams WHERE team_name = "Cowboys"),
    34,25,261,3,0,2,-1,0,0,0,0,0,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Bryce" AND last_name = "Young"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    55,35,328,3,1,2,2,0,0,0,0,0,0,1
  UNION
  SELECT
      (SELECT player_id FROM Players WHERE first_name = "Rico" AND last_name = "Dowdle"),
      (SELECT game_id FROM Games WHERE home_team_id = 
        (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
        away_team_id = 
        (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
        year = "2025" AND week_number = 2),
      (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
      0,0,0,0,0,6,9,0,1,10,0,1,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Tetairoa" AND last_name = "McMillan"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    0,0,0,0,0,0,0,0,6,100,0,10,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Chuba" AND last_name = "Hubbard"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
    0,0,0,0,0,10,38,0,5,39,1,6,0,0
  UNION
  SELECT
  (SELECT player_id FROM Players WHERE first_name = "Tommy" AND last_name = "Tremble"),
  (SELECT game_id FROM Games WHERE home_team_id = 
    (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
    away_team_id = 
    (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
    year = "2025" AND week_number = 2),
  (SELECT team_id FROM Teams WHERE team_name = "Panthers"),
  0,0,0,0,0,0,0,0,3,20,0,3,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Jacoby" AND last_name = "Brissett"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,1,2,0,0,0,0,0,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Emari" AND last_name = "Demercado"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Marvin" AND last_name = "Harrison"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,0,0,0,2,27,0,5,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Trey" AND last_name = "McBride"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,0,0,0,6,78,0,7,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "James" AND last_name = "Conner"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    0,0,0,0,0,11,34,1,1,18,0,1,0,0
  UNION
  SELECT
    (SELECT player_id FROM Players WHERE first_name = "Kyler" AND last_name = "Murray"),
    (SELECT game_id FROM Games WHERE home_team_id = 
      (SELECT team_id FROM Teams WHERE team_name ="Cardinals") AND 
      away_team_id = 
      (SELECT team_id FROM Teams WHERE team_name = "Panthers") AND 
      year = "2025" AND week_number = 2),
    (SELECT team_id FROM Teams WHERE team_name = "Cardinals"),
    25,17,220,1,1,7,32,0,0,0,0,0,0,0;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;