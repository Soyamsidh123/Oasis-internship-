CREATE DATABASE bmi_database;

USE bmi_database;

CREATE TABLE bmi_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    bmi FLOAT NOT NULL,
    category VARCHAR(50)
);
