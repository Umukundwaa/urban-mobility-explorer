ALTER TABLE trip_records
ADD CONSTRAINT positive_distance
CHECK (trip_distance >= 0);

ALTER TABLE trip_records
ADD CONSTRAINT positive_fare
CHECK (fare_amount >= 0);

ALTER TABLE trip_records
ADD CONSTRAINT positive_tip
CHECK (tip_amount >= 0);

ALTER TABLE trip_records
ADD CONSTRAINT positive_total
CHECK (total_amount >= 0);

ALTER TABLE trip_records
ADD CONSTRAINT positive_passengers
CHECK (passenger_count >= 0);