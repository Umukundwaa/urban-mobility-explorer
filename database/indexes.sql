CREATE INDEX idx_pickup_time
ON trip_records(pickup_datetime);

CREATE INDEX idx_dropoff_time
ON trip_records(dropoff_datetime);

CREATE INDEX idx_pickup_zone
ON trip_records(pickup_location_id);

CREATE INDEX idx_dropoff_zone
ON trip_records(dropoff_location_id);

CREATE INDEX idx_total_amount
ON trip_records(total_amount);