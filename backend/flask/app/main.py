from flask import Flask

# ...existing code if any...


def create_app() -> Flask:
    """Flask application factory.

    Wires configuration and route registration. Extend as needed.
    """
    app = Flask(__name__)

    # Import config lazily to avoid circulars
    try:
        from . import config as app_config  # type: ignore
        if hasattr(app_config, "Config"):
            app.config.from_object(app_config.Config)
    except Exception:
        # Fall back to default config if custom config is missing/broken
        pass

    # Register blueprints from routes package if present
    try:
        from .routes import register_routes  # type: ignore
        register_routes(app)
    except Exception:
        # You can later add a register_routes(app) helper in routes/__init__.py
        pass

    return app


def run_api() -> None:
    """Entry point for running the HTTP API service."""
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


def run_mqtt() -> None:
    """Entry point for running the MQTT worker/service.

    Replace the body of this function with your actual MQTT client setup.
    """
    # Lazy import to keep Flask deps separate from MQTT deps if desired
    try:
        from .utils import mqtt_worker  # type: ignore
        mqtt_worker.run()
    except Exception:
        # Placeholder: no-op for now so `SERVICE=mqtt` doesn't crash hard
        print("MQTT service not implemented yet. Implement backend.flask.app.utils.mqtt_worker.run().")
