from flask import Flask, request, make_response, url_for, g
from urllib.parse import urlparse
from http import HTTPStatus
from flask_login import LoginManager
from sqlalchemy import MetaData

login_manager = LoginManager()


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
        app.config["SERVER_NAME"] = "flow2and4.me"
        # Tell Flask it is Behind a Proxy
        # https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

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

    from csduck.rodi.views import bp as bp_rodi

    app.register_blueprint(bp_rodi)

    from csduck.faduck.views import bp as bp_faduck

    app.register_blueprint(bp_faduck, subdomain="faduck")

    from csduck.pyduck.views import bp as bp_pyduck

    app.register_blueprint(bp_pyduck, subdomain="pyduck")

    # Register blueprints [END]

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
    from csduck.auth.service import get_user_for_session
    from csduck.pyduck.auth.service import get_pyduck_user_for_session

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if "pyduck" in urlparse(request.root_url).netloc:
            return get_pyduck_user_for_session(id=int(user_id))

        return get_user_for_session(id=int(user_id))

    # Customize the login process.
    @login_manager.unauthorized_handler
    def unauthorized():
        # TODO: This is not safe.
        next_ = request.referrer if request.referrer else None

        res = make_response()
        res.headers["HX-Reswap"] = "none"
        res.headers["HX-Trigger"] = "login-required"
        return res

    # Register extensions [END]

    return app
