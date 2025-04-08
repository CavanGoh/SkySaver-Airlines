CREATE DATABASE notification_db;
USE notification_db;

-- Create the notifications table
CREATE TABLE notifications (
    notification_id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    flight_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seen BOOLEAN DEFAULT FALSE,
    seen_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    flex_id INTEGER NOT NULL
);

ALTER TABLE notifications ADD COLUMN seat_id VARCHAR(10);
-- Create indexes for better performance
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_flight_id ON notifications(flight_id);
CREATE INDEX idx_notifications_is_active ON notifications(is_active);

