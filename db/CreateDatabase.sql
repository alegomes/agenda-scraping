--  create database agenda_scraping;

USE agenda_scraping;

CREATE TABLE productions (
    created_at DATETIME NOT NULL,
    city VARCHAR(255) NOT NULL,
    theater VARCHAR(255) NOT NULL,
    id VARCHAR(255) NOT NULL,
    showname VARCHAR(255) NOT NULL,
    startdate DATE NOT NULL,
    enddate DATE,
    url VARCHAR(255) NOT NULL,
    CONSTRAINT pk_production PRIMARY KEY (created_at, city, theater, showname, startdate)
);

-- mysql> desc production;
-- +------------+--------------+------+-----+---------+-------+
-- | Field      | Type         | Null | Key | Default | Extra |
-- +------------+--------------+------+-----+---------+-------+
-- | created_at | datetime     | NO   | PRI | NULL    |       |
-- | city       | varchar(255) | NO   | PRI | NULL    |       |
-- | theater    | varchar(255) | NO   | PRI | NULL    |       |
-- | id         | varchar(255) | NO   |     | NULL    |       |
-- | showname   | varchar(255) | NO   | PRI | NULL    |       |
-- | startdate  | date         | NO   |     | NULL    |       |
-- | enddate    | date         | YES  |     | NULL    |       |
-- | url        | varchar(255) | NO   |     | NULL    |       |
-- +------------+--------------+------+-----+---------+-------+
-- 8 rows in set (0.00 sec)

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;
