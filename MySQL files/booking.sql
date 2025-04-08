CREATE DATABASE IF NOT EXISTS booking;
use booking;
DROP TABLE IF EXISTS `booking`;
CREATE TABLE IF NOT EXISTS booking (
    user_id INT NOT NULL,
    booking_id INT NOT NULL AUTO_INCREMENT,
    flight_id INT NOT NULL,
    seat_id VARCHAR(50),
    status VARCHAR(50) NOT NULL,
    PRIMARY KEY (booking_id)
);

-- INSERT INTO Booking (user_id, flight_id, status) VALUES
-- (101, 5001,'' ,'Confirmed'),
-- (102, 5002,'', 'Pending'),
-- (103, 5003,'', 'Cancelled'),
-- (104, 5004,'', 'Confirmed'),
-- (105, 5005,'', 'Pending');