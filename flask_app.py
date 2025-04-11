from flask import Flask, render_template, request
from app.models import db, Usuario, Modulo, Carrito
from flask_login import LoginManager
from app.forms import RegistroForm

login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ava.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # 🔹 Rutas principales aquí:
    @app.route('/')
    def index():
        return "¡Hola! La app Flask está corriendo correctamente en Render 🚀"

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistroForm()
        if form.validate_on_submit():
            return "Registro exitoso"
        return render_template("registro.html", form=form)

    return app

