import os

if __name__ == "__main__":
    service = os.getenv("SERVICE", "api").lower()
    if service == "api":
        from backend.flask.app.main import run_api
        run_api()
    elif service == "mqtt":
        from backend.flask.app.main import run_mqtt
        run_mqtt()
    else:
        raise SystemExit(f"Unknown SERVICE '{service}'. Use 'api' or 'mqtt'.")