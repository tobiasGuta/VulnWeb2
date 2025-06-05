CREATE DATABASE IF NOT EXISTS blind_sqli;
USE blind_sqli;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  password VARCHAR(50)
);

INSERT INTO users (username, password) VALUES 
('admin', 'supersecret'),
('john', 'johnpass'),
('alice', 'alicepass');
