CREATE DATABASE IF NOT EXISTS vulnapp;

USE vulnapp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255)
);

INSERT INTO users (username, password) VALUES 
('admin', 'supersecret'),
('guest', 'guestpass');
