from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from forms import RegistroForm, LoginForm
from models import db, Usuario, Modulo, Carrito

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ava.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de base de datos y login
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas principales
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistroForm()
    if form.validate_on_submit():
        usuario_existente = Usuario.query.filter_by(correo=form.correo.data).first()
        if usuario_existente:
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('register'))
        usuario = Usuario(nombre=form.nombre.data, correo=form.correo.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Registro exitoso. Inicia sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard'))
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    modulos = Modulo.query.all()
    return render_template('dashboard.html', modulos=modulos)

@app.route('/modulo/<int:id>')
@login_required
def modulo(id):
    modulo = Modulo.query.get_or_404(id)
    return render_template('modulo.html', modulo=modulo)

# Carrito de compras
@app.route('/agregar_carrito/<int:id>')
@login_required
def agregar_carrito(id):
    modulo = Modulo.query.get_or_404(id)
    existente = Carrito.query.filter_by(usuario_id=current_user.id, modulo_id=id).first()
    if existente:
        flash('Este módulo ya está en tu carrito.', 'warning')
    else:
        carrito = Carrito(usuario_id=current_user.id, modulo_id=id)
        db.session.add(carrito)
        db.session.commit()
        flash('Módulo agregado al carrito.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/carrito')
@login_required
def carrito():
    items = Carrito.query.filter_by(usuario_id=current_user.id).all()
    return render_template('carrito.html', items=items)

@app.route('/eliminar_carrito/<int:id>')
@login_required
def eliminar_carrito(id):
    item = Carrito.query.get_or_404(id)
    if item.usuario_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash('Módulo eliminado del carrito.', 'info')
    else:
        flash('No tienes permiso para eliminar este módulo.', 'danger')
    return redirect(url_for('carrito'))

# Crear la base de datos, módulos de prueba y usuario demo
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Crear módulos demo si no existen
        if not Modulo.query.first():
            modulos_demo = [
                Modulo(
                    nombre='Introducción A La Computación Cuántica',
                    descripcion='Qué es\nHistoria\nImportancia de uso',
                    precio=100.000
                ),
                Modulo(
                    nombre='Puertas cuánticas',
                    descripcion='Operaciones fundamentales Tipos de puertas: X, Y, Z, Hadamard',
                    precio=200.0000
                ),
                Modulo(
                    nombre='Algoritmos cuánticos',
                    descripcion='Algoritmos como Grover y Shor\nAplicaciones prácticas',
                    precio=400.000
                )
            ]
            db.session.add_all(modulos_demo)

        # Crear usuario demo si no existe
        if not Usuario.query.filter_by(correo='test@correo.com').first():
            usuario_demo = Usuario(nombre='Compu', correo='test@correo.com')
            usuario_demo.set_password('1234')
            db.session.add(usuario_demo)

        db.session.commit()

    app.run(debug=True)
