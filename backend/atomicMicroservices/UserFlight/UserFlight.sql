CREATE DATABASE IF NOT EXISTS UserFlight;
use UserFlight;
CREATE TABLE UserFlight (
    user_id INT NOT NULL,
    flight_id INT NOT NULL,
    PRIMARY KEY (user_id, flight_id)
);

INSERT INTO UserFlight (user_id, flight_id) VALUES
(101, 5001);