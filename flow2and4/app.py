from flask import Flask, request, make_response, url_for, g
from urllib.parse import urlparse
from http import HTTPStatus
from flask_login import LoginManager
from sqlalchemy import MetaData

login_manager = LoginManager()


def create_app(mode: str = "dev"):
    """Create flask application."""

    app = Flask(__name__, subdomain_matching=True)

    from flow2and4.config import WebConfig

    app.config.from_object(WebConfig())

    if mode == "dev":
        app.config["SERVER_NAME"] = "localhost:5000"

    if mode == "test":
        from flow2and4.config import WebTestConfig

        app.config.from_object(WebTestConfig())

    if mode == "prod":
        from flow2and4.config import WebProdConfig
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.config.from_object(WebProdConfig())
        app.config["SERVER_NAME"] = "flow2and4.me"
        # Tell Flask it is Behind a Proxy
        # https://flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # [START] Register blueprints
    from flow2and4.views import bp as bp
    from flow2and4.auth.views import bp as bp_auth
    from flow2and4.duckwave_ms.views import bp as bp_duckwave_ms
    from flow2and4.duckwave_os.views import bp as bp_duckwave_os
    from flow2and4.duckwave_pg.views import bp as bp_duckwave_pg
    from flow2and4.duckwave_cn.views import bp as bp_duckwave_cn

    app.register_blueprint(bp, subdomain="csduck")
    app.register_blueprint(bp_auth, subdomain="csduck")
    app.register_blueprint(bp_duckwave_ms, subdomain="csduck")
    app.register_blueprint(bp_duckwave_os, subdomain="csduck")
    app.register_blueprint(bp_duckwave_pg, subdomain="csduck")
    app.register_blueprint(bp_duckwave_cn, subdomain="csduck")

    from flow2and4.rodi.views import bp as bp_rodi

    app.register_blueprint(bp_rodi)

    from flow2and4.faduck.views import bp as bp_faduck

    app.register_blueprint(bp_faduck, subdomain="faduck")

    from flow2and4.pyduck.views import bp as bp_pyduck

    app.register_blueprint(bp_pyduck, subdomain="pyduck")

    # Register blueprints [END]

    # [START] Register extensions
    from flask_wtf import CSRFProtect
    from flow2and4.database import db, migrate

    # CSRF protection.
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Database.
    db.init_app(app)
    migrate.init_app(app, db)

    # Database____sqlite specific foreign key enabled.
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute("PRAGMA foreign_keys=ON")

    with app.app_context():
        from sqlalchemy import event

        for _engine in db.engines.values():
            event.listen(_engine, "connect", _fk_pragma_on_connect)

    # Bcrypt.
    from flask_bcrypt import Bcrypt

    bcrypt = Bcrypt()
    bcrypt.init_app(app)

    # Login.
    from flow2and4.auth.service import get_user_for_session
    from flow2and4.pyduck.auth.service import get_pyduck_user_for_session

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
