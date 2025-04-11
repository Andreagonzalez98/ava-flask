from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(128))

    def set_password(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)

    def check_password(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)

class Modulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'))

    usuario = db.relationship('Usuario', backref='carritos')
    modulo = db.relationship('Modulo')
