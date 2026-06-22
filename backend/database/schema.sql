-- ================================================
-- URBAN MOBILITY EXPLORER
-- schema.sql - Create Tables + Indexes
-- ================================================

CREATE TABLE IF NOT EXISTS zones (
    location_id INT PRIMARY KEY,
    borough VARCHAR(50) NOT NULL,
    zone_name VARCHAR(100) NOT NULL,
    service_zone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id INT,
    pickup_datetime DATETIME NOT NULL,
    dropoff_datetime DATETIME NOT NULL,
    passenger_count INT,
    trip_distance FLOAT,
    rate_code_id INT,
    pickup_location_id INT,
    dropoff_location_id INT,
    payment_type INT,
    fare_amount FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    total_amount FLOAT,
    congestion_surcharge FLOAT DEFAULT 0,
    trip_duration_minutes FLOAT,
    fare_per_mile FLOAT,
    time_of_day VARCHAR(20),
    FOREIGN KEY (pickup_location_id) REFERENCES zones(location_id),
    FOREIGN KEY (dropoff_location_id) REFERENCES zones(location_id)
);

CREATE INDEX idx_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX idx_pickup_location ON trips(pickup_location_id);
CREATE INDEX idx_dropoff_location ON trips(dropoff_location_id);
CREATE INDEX idx_time_of_day ON trips(time_of_day);