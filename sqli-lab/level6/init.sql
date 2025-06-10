CREATE DATABASE IF NOT EXISTS vulnapp;
USE vulnapp;

CREATE TABLE IF NOT EXISTS logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(255),
    user_agent TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255)
);

INSERT INTO user (username, password) VALUES
('admin', 'supersecrethash'),
('guest', 'guestpass');

INSERT INTO logins (ip, user_agent, note)
VALUES ('127.0.0.1', 'TestAgent', 'Initial entry');
