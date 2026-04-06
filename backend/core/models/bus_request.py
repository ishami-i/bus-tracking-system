''' 
This is the bus request moidels which contains s
request_id SERIAL PRIMARY KEY,
    request_code TEXT GENERATED ALWAYS AS ('request-' || id) STORED stop_id INT REFERENCES stops (stop_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    passenger_status VARCHAR(50), -- e.g. 'pending', 'picked_up', 'cancelled'
    request_time TIMESTAMP NOT NULL DEFAULT NOW()
'''


