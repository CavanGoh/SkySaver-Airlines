
CREATE DATABASE IF NOT EXISTS `user` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


USE `user`;


DROP TABLE IF EXISTS `users`;


CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `name` VARCHAR(120) NULL,
  PRIMARY KEY (`id`),
  INDEX `email_index` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO users (email, password) VALUES
('tanedric@gmail.com','123')
