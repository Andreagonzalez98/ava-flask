from flask_app import create_app
from app.models import db, Modulo, Usuario

app = create_app()

with app.app_context():
    db.create_all()

    if not Modulo.query.first():
        modulos_demo = [
            Modulo(nombre='Introducción A La Computación Cuántica',
                   descripcion='Qué es\nHistoria\nImportancia de uso',
                   precio=100.000),
            Modulo(nombre='Puertas cuánticas',
                   descripcion='Operaciones fundamentales Tipos de puertas: X, Y, Z, Hadamard',
                   precio=200.000),
            Modulo(nombre='Algoritmos cuánticos',
                   descripcion='Algoritmos como Grover y Shor\nAplicaciones prácticas',
                   precio=400.000)
        ]
        db.session.add_all(modulos_demo)

    if not Usuario.query.filter_by(correo='test@correo.com').first():
        usuario_demo = Usuario(nombre='Demo', correo='test@correo.com')
        usuario_demo.set_password('1234')
        db.session.add(usuario_demo)

    db.session.commit()
    print("Base de datos inicializada.")
