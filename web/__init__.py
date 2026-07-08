from flask import Flask, render_template
import mongoengine
from bson.objectid import ObjectId
from flask_login import LoginManager
from config import Config
import firebase_admin
from firebase_admin import credentials


# LOGIN MANAGER CLASS
login_manager = LoginManager()


def create_app():
    # CREATE A FLASK INSTANCE
    app = Flask(__name__)
    app.config.from_object(Config)

    # FIREBASE SETUP
    if not firebase_admin._apps:
        cred_path = app.config["FIREBASE_CRED_PATH"]
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)


    # INIT DATABASE
    mongoengine.connect(
        # db='miniart_v2', # production only
        host=app.config['MONGO_URI']
    )

    
    # IMPORT ROUTE BLUEPRINTS
    from .auth import auth
    from .root import root
    from .routes import routes
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')


    # CALL CREATE DB FUNCTION
    # FOR MONGODB
    create_mongo_db(app)


    # LOGIN MANAGER CONFIG
    # INITIALIZE LM
    login_manager.init_app(app)
    
    # CUSTOMIZE LM
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page!"
    login_manager.login_message_category = 'warning'

    # IMPORT USERS MODEL
    from .models import Users

    # LOAD USERS
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return Users.objects.get(id=ObjectId(user_id))
        except:
            return None


    # CREATE CUSTOM ERROR PAGES
    # BAD REQUEST ERROR
    @app.errorhandler(400)
    def bad_request(e):
        return render_template ('errors/400.html'), 400

    # UNAUTHORIZED ERROR
    @app.errorhandler(401)
    def unauthorized_error(e):
        return render_template ('errors/401.html'), 401
    
    # NOT FOUND ERROR
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template ('errors/404.html'), 404

    # INTERNAL SERVER ERROR
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template ('errors/500.html'), 500
    


    return app


# CREATE MONGO DB
def create_mongo_db(app):
    with app.app_context():
        from .models import Users, AuthMethods

        admin_email = app.config["ADMIN_EMAIL"]
        admin_pass = app.config["ADMIN_PASS"]

        admin = Users.objects(email=admin_email).first()

        if not admin:
            admin_user = Users(
                name = "Admin",
                email = admin_email,
                role = "admin"
            )
            admin_user.save()

            # Create local auth
            admin_auth_local = AuthMethods(
                user_id = admin_user,
                provider = "local",
                username = "admin",
            )
            admin_auth_local.password = admin_pass
            try:
                admin_auth_local.save()
            except Exception as e:
                print("LOCAL AUTH ERROR:", e)

            print("\n✅ Admin User Created!\n")
        else:
            print("\n✅ Admin Already Exists!\n")