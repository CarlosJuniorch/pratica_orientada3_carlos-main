from flask import Flask, render_template, request, url_for, redirect, session
from sqlalchemy import select

from database import Base, session, engine
from models import Livro, Usuario

app = Flask(__name__)
Base.metadata.create_all(engine)

app.secret_key = 'hugulei'

@app.route('/')
def index():
    with session:
        usuarios = session.scalars(select(Usuario.nome)).all()
        livros = session.scalars(select(Livro.titulo)).all()
    return render_template('index.html', usuario=usuarios, livro=livros)


@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = Usuario(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with session:
            session.add(usuario)
            session.commit()
        return redirect(url_for('index'))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    with session:
        usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
        if request.method == 'POST':
            livro = Livro(
                titulo=request.form.get('titulo'),
                usuario_id=int(request.form.get('usuario_id'))
            )
            session.add(livro)
            session.commit()
            return redirect(url_for('index'))
    return render_template('form_livro.html', usuario=usuarios)

@app.route('/livros/listar', methods=['GET'])
def listar_livros():
    with session:
        statement = select(Livro).order_by(Livro.titulo)
        livros = session.scalars(statement).all()
        
        return render_template('index.html', livros=livros)

@app.route('/usuarios/listar', methods=['GET'])
def listar_usuarios():
    with session:
        statement = select(Usuario).order_by(Usuario.nome)
        usuarios = session.scalars(statement).all()

        return render_template('index.html', usuario=usuarios)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('form_usuario'))
        
if __name__ == "__main__":
    app.run(debug=True)