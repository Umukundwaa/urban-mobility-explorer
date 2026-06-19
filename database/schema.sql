CREATE TABLE zones (
    location_id INTEGER PRIMARY KEY,
    borough VARCHAR(100),
    zone VARCHAR(150),
    service_zone VARCHAR(150)
);
CREATE TABLE trip_records (

    trip_id BIGSERIAL PRIMARY KEY,

    pickup_datetime TIMESTAMP NOT NULL,

    dropoff_datetime TIMESTAMP NOT NULL,

    passenger_count INTEGER,

    trip_distance DECIMAL(10,2),

    fare_amount DECIMAL(10,2),

    tip_amount DECIMAL(10,2),

    total_amount DECIMAL(10,2),

    payment_type INTEGER,

    pickup_location_id INTEGER,

    dropoff_location_id INTEGER,

    FOREIGN KEY (pickup_location_id)
        REFERENCES zones(location_id),

    FOREIGN KEY (dropoff_location_id)
        REFERENCES zones(location_id)
);

CREATE TABLE trip_features (

    trip_id BIGINT PRIMARY KEY,

    trip_duration_minutes DECIMAL(10,2),

    average_speed DECIMAL(10,2),

    fare_per_mile DECIMAL(10,2),

    FOREIGN KEY (trip_id)
        REFERENCES trip_records(trip_id)
);

CREATE TABLE zone_geometry (

    location_id INTEGER PRIMARY KEY,

    geometry JSONB,

    FOREIGN KEY (location_id)
        REFERENCES zones(location_id)
);

CREATE TABLE data_quality_log (

    log_id SERIAL PRIMARY KEY,

    trip_identifier VARCHAR(100),

    issue_type VARCHAR(100),

    description TEXT,

    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);