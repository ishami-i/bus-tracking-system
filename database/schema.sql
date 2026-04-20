/* 
This is the schema file for table and bus_system_db.
It defines the structure of the database, including tables, relationships, and constraints.
the PostgreSQL database is used for this project.
the database is designed to support a bus system, including users, drivers, passengers, routes, stops, trips, and related events.
the database is created with a focus on data integrity, performance, and scalability, using appropriate data types, constraints, and indexing strategies.
the bash script with create database and execute this schema file is provided in the database directory.
*/

-- USERS (base identity)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_code TEXT GENERATED ALWAYS AS ('user-' || user_id) STORED,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    role VARCHAR(50) NOT NULL CHECK (
        role IN (
            'admin',
            'driver',
            'passenger',
            'sales',
            'coordinator'
        )
    )
);

-- DRIVERS (specialized users)

CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_code TEXT GENERATED ALWAYS AS ('driver-' || driver_id) STORED,
    user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    bus_id INT
);

-- PASSENGERS (specialized users)

CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    passenger_code TEXT GENERATED ALWAYS AS ('passenger-' || passenger_id) STORED,
    user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    tap_go_number VARCHAR(50) UNIQUE
);

-- ROUTES

CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    route_code TEXT GENERATED ALWAYS AS ('route-' || route_id) STORED,
    name VARCHAR(100) NOT NULL,
    starting_address VARCHAR(255),
    starting_longitude DECIMAL(10, 7),
    starting_latitude DECIMAL(10, 7),
    ending_address VARCHAR(255),
    ending_longitude DECIMAL(10, 7),
    ending_latitude DECIMAL(10, 7)
);

-- STOPS

CREATE TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    stop_code TEXT GENERATED ALWAYS AS ('stop-' || stop_id) STORED,
    stop_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    longitude DECIMAL(10, 7),
    latitude DECIMAL(10, 7)
);

-- ROUTE_STOPS (ordering)

CREATE TABLE route_stops (
    route_stop_id SERIAL PRIMARY KEY,
    route_id INT NOT NULL REFERENCES routes (route_id) ON DELETE CASCADE,
    stop_id INT NOT NULL REFERENCES stops (stop_id) ON DELETE CASCADE,
    stop_order INT NOT NULL,
    UNIQUE (route_id, stop_order)
);

-- BUSES

CREATE TABLE buses (
    bus_id SERIAL PRIMARY KEY,
    bus_code TEXT GENERATED ALWAYS AS ('bus-' || bus_id) STORED,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    bus_capacity INT NOT NULL CHECK (bus_capacity > 0),
    bus_status VARCHAR(50) NOT NULL CHECK (
        bus_status IN (
            'active',
            'maintenance',
            'decommissioned'
        )
    ),
    route_id INT REFERENCES routes (route_id) ON DELETE SET NULL
);

-- TRIPS (core operational unit)

CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    trip_code TEXT GENERATED ALWAYS AS ('trip-' || trip_id) STORED,
    route_id INT REFERENCES routes (route_id) ON DELETE SET NULL,
    driver_id INT REFERENCES drivers (driver_id) ON DELETE SET NULL,
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL,
    event_id INT,
    starting_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (
        status IN (
            'scheduled',
            'in_progress',
            'completed',
            'cancelled'
        )
    )
);

-- PASSENGER EVENTS (tap in/out)

CREATE TABLE passenger_events (
    event_id SERIAL PRIMARY KEY,
    event_code TEXT GENERATED ALWAYS AS ('event-' || event_id) STORED,
    trip_id INT NOT NULL REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT NOT NULL REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (
        event_type IN ('tap_on', 'tap_off')
    ),
    event_time TIMESTAMP NOT NULL DEFAULT NOW()
);

-- GPS LOGS (history tracking)

CREATE TABLE gps_logs (
    log_id SERIAL PRIMARY KEY,
    log_code TEXT GENERATED ALWAYS AS ('gpslog-' || log_id) STORED,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE SET NULL
);

-- BUS REQUESTS (stop requests)

CREATE TABLE bus_requests (
    request_id SERIAL PRIMARY KEY,
    request_code TEXT GENERATED ALWAYS AS ('request-' || request_id) STORED,
    stop_id INT REFERENCES stops (stop_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    request_status VARCHAR(50) CHECK (
        request_status IN (
            'pending',
            'picked_up',
            'cancelled'
        )
    ),
    request_time TIMESTAMP NOT NULL DEFAULT NOW()
);

-- INDEXES (performance)

CREATE INDEX idx_gps_bus ON gps_logs (bus_id);

CREATE INDEX idx_gps_trip ON gps_logs (trip_id);

CREATE INDEX idx_trip_route ON trips (route_id);

CREATE INDEX idx_trip_driver ON trips (driver_id);

CREATE INDEX idx_passenger_trip ON passenger_events (trip_id);

ALTER TABLE drivers
ADD CONSTRAINT fk_drivers_bus
FOREIGN KEY (bus_id) REFERENCES buses (bus_id) ON DELETE SET NULL;