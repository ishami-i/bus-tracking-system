-- BUS SYSTEM DATABASE SCHEMA
-- create the database
CREATE DATABASE IF NOT EXISTS bus_system;
-- using the database
USE bus_system;
-- Users (base identity table)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_code TEXT GENERATED ALWAYS AS ('user-' || id) STORED name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telephone VARCHAR(20),
    role VARCHAR(50) NOT NULL -- e.g. 'admin', 'driver', 'passenger'
);

-- Routes
CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    route_code TEXT GENERATED ALWAYS AS ('route-' || id) STORED name VARCHAR(100) NOT NULL,
    starting_address VARCHAR(255),
    starting_longitude DECIMAL(10, 7),
    starting_latitude DECIMAL(10, 7),
    ending_address VARCHAR(255),
    ending_longitude DECIMAL(10, 7),
    ending_latitude DECIMAL(10, 7)
);

-- Buses
CREATE TABLE buses (
    bus_id SERIAL PRIMARY KEY,
    bus_code TEXT GENERATED ALWAYS AS ('bus-' || id) STORED bus_plate VARCHAR(20) UNIQUE NOT NULL,
    bus_capacity INT NOT NULL,
    route_id INT REFERENCES routes (route_id) ON DELETE SET NULL
);

-- Drivers (linked to a user and assigned a bus)
CREATE TABLE drivers (
    driver_id SERIAL PRIMARY KEY,
    driver_code TEXT GENERATED ALWAYS AS ('driver-' || id) STORED user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL
);

-- Passengers (linked to a user)
CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    passenger_code TEXT GENERATED ALWAYS AS ('passenger-' || id) STORED user_id INT NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    tap_go_number VARCHAR(50) UNIQUE -- transit card / tap-and-go identifier
);

-- Stops (physical bus stop locations)
CREATE TABLE stops (
    stop_id SERIAL PRIMARY KEY,
    stop_code TEXT GENERATED ALWAYS AS ('stop-' || id) STORED stop_name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    longitude DECIMAL(10, 7),
    latitude DECIMAL(10, 7) -- note: ERD shows "lotitude" — corrected to latitude
);

-- Route Stops (many-to-many: which stops belong to which route, in what order)
CREATE TABLE route_stops (
    route_stop_id SERIAL PRIMARY KEY,
    stop_id INT NOT NULL REFERENCES stops (stop_id) ON DELETE CASCADE,
    route_id INT NOT NULL REFERENCES routes (route_id) ON DELETE CASCADE,
    stop_order INT NOT NULL
);

-- Trips (a scheduled run of a route by a driver)
CREATE TABLE trips (
    trip_id SERIAL PRIMARY KEY,
    trip_code TEXT GENERATED ALWAYS AS ('trip-' || id) STORED route_id INT REFERENCES routes (route_id) ON DELETE SET NULL,
    driver_id INT REFERENCES drivers (driver_id) ON DELETE SET NULL,
    event_id INT, -- FK to passenger_events (set after table creation)
    starting_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL -- e.g. 'scheduled', 'in_progress', 'completed', 'cancelled'
);

-- Passenger Events (tap-on / tap-off events during a trip)
CREATE TABLE passenger_events (
    event_id SERIAL PRIMARY KEY,
    event_code TEXT GENERATED ALWAYS AS ('event-' || id) STORED trip_id INT NOT NULL REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT NOT NULL REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- e.g. 'tap_on', 'tap_off'
    event_time TIMESTAMP NOT NULL
);

-- Add the FK from trips.event_id → passenger_events.event_id (circular ref, deferred)
ALTER TABLE trips
ADD CONSTRAINT fk_trips_event FOREIGN KEY (event_id) REFERENCES passenger_events (event_id) DEFERRABLE INITIALLY DEFERRED;

-- GPS Logs (real-time location tracking per bus/trip)
CREATE TABLE gps_logs (
    log_id SERIAL PRIMARY KEY,
    log_code TEXT GENERATED ALWAYS AS ('gpslog-' || id) STORED longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    timestamps TIMESTAMP NOT NULL DEFAULT NOW(),
    bus_id INT REFERENCES buses (bus_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE SET NULL
);

-- Bus Requests (passenger requests to board at a stop on a trip)
CREATE TABLE bus_requests (
    request_id SERIAL PRIMARY KEY,
    request_code TEXT GENERATED ALWAYS AS ('request-' || id) STORED stop_id INT REFERENCES stops (stop_id) ON DELETE SET NULL,
    trip_id INT REFERENCES trips (trip_id) ON DELETE CASCADE,
    passenger_id INT REFERENCES passengers (passenger_id) ON DELETE CASCADE,
    passenger_status VARCHAR(50), -- e.g. 'pending', 'picked_up', 'cancelled'
    request_time TIMESTAMP NOT NULL DEFAULT NOW()
);

-- INDEXES (recommended for FK columns used in JOINs)
CREATE INDEX idx_buses_route_id ON buses (route_id);

CREATE INDEX idx_drivers_user_id ON drivers (user_id);

CREATE INDEX idx_drivers_bus_id ON drivers (bus_id);

CREATE INDEX idx_passengers_user_id ON passengers (user_id);

CREATE INDEX idx_route_stops_route_id ON route_stops (route_id);

CREATE INDEX idx_route_stops_stop_id ON route_stops (stop_id);

CREATE INDEX idx_trips_route_id ON trips (route_id);

CREATE INDEX idx_trips_driver_id ON trips (driver_id);

CREATE INDEX idx_passenger_events_trip_id ON passenger_events (trip_id);

CREATE INDEX idx_passenger_events_pax_id ON passenger_events (passenger_id);

CREATE INDEX idx_gps_logs_bus_id ON gps_logs (bus_id);

CREATE INDEX idx_gps_logs_trip_id ON gps_logs (trip_id);

CREATE INDEX idx_bus_requests_trip_id ON bus_requests (trip_id);

CREATE INDEX idx_bus_requests_pax_id ON bus_requests (passenger_id);

CREATE INDEX idx_bus_requests_stop_id ON bus_requests (stop_id);