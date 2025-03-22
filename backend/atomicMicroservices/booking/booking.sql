CREATE DATABASE IF NOT EXISTS booking;
use booking;
CREATE TABLE booking (
    user_id INT NOT NULL,
    booking_id INT NOT NULL AUTO_INCREMENT,
    flight_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    PRIMARY KEY (booking_id)
);

INSERT INTO Booking (user_id, flight_id, status) VALUES
(101, 5001, 'Confirmed'),
(102, 5002, 'Pending'),
(103, 5003, 'Cancelled'),
(104, 5004, 'Confirmed'),
(105, 5005, 'Pending');