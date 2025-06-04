DROP DATABASE IF EXISTS sqli_one;
CREATE DATABASE sqli_one;
USE sqli_one;

CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT
);

INSERT INTO articles (title, content) VALUES
('Welcome to SQLi Lab', 'This is the first article in your training.'),
('Understanding UNION SELECT', 'You are progressing well.');

CREATE TABLE staff_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(100)
);

INSERT INTO staff_users (username, password) VALUES
('martin', 'hunter2'),
('root', 'toor1337');
