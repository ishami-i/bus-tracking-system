import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "bus_system")
    DB_USER = os.getenv("DB_USER", "bus_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    # MQTT
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "bus-tracking-backend")
