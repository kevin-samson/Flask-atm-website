from flask import Flask
from flask_mail import Mail
from atm.config import Config

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    from atm.users.routes import user
    from atm.bank.routes import bank
    from atm.main.routes import main
    from atm.admin.routes import admin
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(bank)
    app.register_blueprint(main)

    return app
