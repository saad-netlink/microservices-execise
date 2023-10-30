-- Create the authdb database
CREATE DATABASE IF NOT EXISTS authdb;

-- Use the authdb database
USE authdb;

-- Create the auth_table
CREATE TABLE `auth` (
  `id` VARCHAR(128) DEFAULT (uuid()),
  `key` VARCHAR(64) NOT NULL,
  `version` INT(9) unsigned NOT NULL AUTO_INCREMENT,
  KEY `id` (`id`),
  KEY `version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Insert a sample row into the auth_table
INSERT INTO auth (`key`) VALUES ('very-secure-passkey');
