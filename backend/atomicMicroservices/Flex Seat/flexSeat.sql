CREATE DATABASE IF NOT EXISTS flexSeat
    CHARACTER SET utf8mb4;
    
USE flexSeat;

DROP TABLE IF EXISTS `flexSeat`;

CREATE TABLE IF NOT EXISTS `flexSeat` (
    `flexId` INT AUTO_INCREMENT PRIMARY KEY,         -- New auto-incrementing primary key
    `userId` INT NOT NULL,                           -- Passenger identifier
    `startDestination` VARCHAR(100) NOT NULL,        -- Departure location
    `endDestination` VARCHAR(100) NOT NULL,          -- Arrival location
    `startDate` DATE NOT NULL,                       -- Start of preferred date range
    `endDate` DATE NOT NULL,                         -- End of preferred date range
    `createdAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the search was created
    UNIQUE KEY `unique_flex_entry` (userId, startDestination, endDestination, startDate, endDate)
) Engine=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flexSeat`
--

-- INSERT INTO `flexSeat` (`userId`, `startDestination`, `endDestination`, `startDate`, `endDate`, `createdAt`) 
-- VALUES 
-- (1, 'Singapore', 'Tokyo', '2025-04-01', '2025-04-01', NOW()),
-- (2, 'New York', 'Los Angeles', '2025-05-10', '2025-05-10', NOW()),
-- (3, 'London', 'Paris', '2025-06-15', '2025-06-15', NOW()),
-- (4, 'Dubai', 'Sydney', '2025-07-20', '2025-07-20', NOW()),
-- (5, 'Berlin', 'Rome', '2025-08-05', '2025-08-05', NOW()),
-- (6, 'New York', 'London', '2025-04-01', '2025-04-30', NOW()),
-- (7, 'New York', 'London', '2025-04-01', '2025-04-30', NOW()),
-- (8, 'New York', 'London', '2025-04-01', '2025-04-30', NOW());
