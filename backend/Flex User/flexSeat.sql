CREATE DATABASE IF NOT EXISTS flexSeat
	CHARACTER SET utf8mb4;
    
USE flexSeat;
DROP TABLE IF EXISTS `flexSeat`;
CREATE TABLE IF NOT EXISTS `flexSeat` (
    `passengerId` INT NOT NULL,                            -- Passenger identifier
    `startDestination` VARCHAR(100) NOT NULL,             -- Departure location
    `endDestination` VARCHAR(100) NOT NULL,               -- Arrival location
    `startDateTime` TIMESTAMP NOT NULL,                   -- Start of preferred time range
    `endDateTime` TIMESTAMP NOT NULL,                     -- End of preferred time range
    `createdAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- Timestamp for when the search was created
    PRIMARY KEY (passengerId, startDestination, endDestination, startDateTime, endDateTime)
) Engine=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flexSeat`
--

INSERT INTO `flexSeat` (`passengerId`, `startDestination`, `endDestination`, `startDateTime`, `endDateTime`, `createdAt`) 
VALUES 
(1, 'Singapore', 'Tokyo', '2025-04-01 08:00:00', '2025-04-01 18:00:00', NOW()),
(2, 'New York', 'Los Angeles', '2025-05-10 06:00:00', '2025-05-10 12:00:00', NOW()),
(3, 'London', 'Paris', '2025-06-15 09:00:00', '2025-06-15 20:00:00', NOW()),
(4, 'Dubai', 'Sydney', '2025-07-20 00:00:00', '2025-07-20 23:59:59', NOW()),
(5, 'Berlin', 'Rome', '2025-08-05 07:30:00', '2025-08-05 15:00:00', NOW());
