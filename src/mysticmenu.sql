CREATE DATABASE mysticburgers_db;

CREATE TABLE mysticburgers (
    Store TEXT,
    Category TEXT,
    Item TEXT,
    Description TEXT,
    Price FLOAT,
    QTY INT,
    Magic BOOLEAN
);

COPY mysticburgers (Store, Category, Item, Description, Price, QTY, Magic)
FROM '/mnt/c/Users/sarah/OneDrive/Desktop/School/2024/Fall/SWDevCS-3250-002/CS3250/Project3/project-3-final-project-thedreamteam2/Database/mysticburgers.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM mysticburgers;