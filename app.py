from apps import create_app
from apps.config import config

app = create_app(config)


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        # ssl_context=app.config["SSL"]
    )
