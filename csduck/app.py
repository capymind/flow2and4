from flask import Flask


def create_app(mode: str = "dev"):
    """Create flask application."""

    app = Flask(__name__, subdomain_matching=True)

    from csduck.config import WebConfig

    app.config.from_object(WebConfig())

    if mode == "dev":
        app.config["SERVER_NAME"] = "localhost:5000"

    if mode == "test":
        from csduck.config import WebTestConfig

        app.config.from_object(WebTestConfig())

    if mode == "prod":
        from csduck.config import WebProdConfig
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.config.from_object(WebProdConfig())
        # Tell Flask it is Behind a Proxy
        # https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # [START] Register extensions
    from flask_wtf import CSRFProtect
    from csduck.database import db, migrate

    # CSRF protection.
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Database.
    db.init_app(app)
    migrate.init_app(app, db)

    # Bcrypt.
    from flask_bcrypt import Bcrypt

    bcrypt = Bcrypt()
    bcrypt.init_app(app)

    # Login.
    from flask_login import LoginManager
    from csduck.auth.service import get_user_for_session

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_for_session(id=int(user_id))

    # Register extensions [END]

    # [START] Register blueprints
    from csduck.views import bp as bp
    from csduck.auth.views import bp as bp_auth
    from csduck.duckwave_ms.views import bp as bp_duckwave_ms
    from csduck.duckwave_os.views import bp as bp_duckwave_os
    from csduck.duckwave_pg.views import bp as bp_duckwave_pg
    from csduck.duckwave_cn.views import bp as bp_duckwave_cn

    app.register_blueprint(bp, subdomain="csduck")
    app.register_blueprint(bp_auth, subdomain="csduck")
    app.register_blueprint(bp_duckwave_ms, subdomain="csduck")
    app.register_blueprint(bp_duckwave_os, subdomain="csduck")
    app.register_blueprint(bp_duckwave_pg, subdomain="csduck")
    app.register_blueprint(bp_duckwave_cn, subdomain="csduck")
    # Register blueprints [END]

    return app
