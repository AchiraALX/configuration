CREATE USER 'holberton_user'@'localhost' IDENTIFIED BY 'projectcorrection280hbtn';

GRANT REPLICATION CLIENT ON *.* TO 'holberton_user'@'localhost';

CREATE DATABASE IF NOT EXISTS tyrell_corp;

GRANT ALL PRIVILEGES ON tyrell_corp.* TO 'holberton_user'@'localhost';

USE tyrell_corp;

-- Create table nexus6
CREATE TABLE IF NOT EXISTS tyrell_corp.nexus6 (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insert values into nexus6
INSERT INTO tyrell_corp.nexus6 (name) VALUES ('Leon'), ('Rachel'), ('Roy'), ('Pris');

CREATE USER 'replica_user'@'%' IDENTIFIED BY '@lazyachiraJ1';

GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';

FLUSH PRIVILEGES;

SELECT User, Repl_slave_priv FROM mysql.user WHERE User='replica_user';