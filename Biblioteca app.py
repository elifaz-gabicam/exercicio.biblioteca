from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# ===============================
# Configuração do Flask e do Banco de Dados
# ===============================

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Definindo uma chave secreta mais segura

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livros.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===============================
# Modelos de Dados
# ===============================

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.username}>"

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    editora = db.Column(db.String(200), default="Sem Editora")
    ativo = db.Column(db.Boolean, default=False)
    reservado = db.Column(db.Boolean, default=False)

    def __init__(self, titulo, autor, categoria, ano, editora="Sem Editora", ativo=False, reservado=False):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano = ano
        self.editora = editora
        self.ativo = ativo
        self.reservado = reservado

    def __repr__(self):
        return f"<Livro {self.titulo}>"

# ===============================
# Funções de Inicialização do Banco de Dados
# ===============================

def init_db():
    with app.app_context():
        db.create_all()

        print("Diretório Atual:", os.getcwd())
        file_path = "D:/exercicios.py/tabela - livros.csv"
        if os.path.exists(file_path):
            print("Arquivo encontrado!")
            df = pd.read_csv(file_path)

            for index, row in df.iterrows():
                if not Livro.query.filter_by(titulo=row.get("Titulo do Livro")).first():
                    livro = Livro(
                        titulo=row.get("Titulo do Livro"),
                        autor=row.get("Autor"),
                        categoria=row.get("Categoria"),
                        ano=row.get("Ano de Publicação"),
                        ativo=row.get("Ativo") == "TRUE",
                    )
                    db.session.add(livro)
            db.session.commit()
        else:
            print("Arquivo não encontrado:", file_path)

def create_test_user():
    """Cria um usuário de teste. Deve ser executada uma vez."""
    with app.app_context():
        if not Usuario.query.filter_by(username='elifaz.gabi@gmail.com').first():
            hashed_password = generate_password_hash('elifazgc2024')
            new_user = Usuario(username='elifaz.gabi@gmail.com', password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

# ===============================
# Rotas da Aplicação
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("inicio"))
        else:
            return "Usuário ou senha inválidos", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    search_query = request.args.get('search', '')

    if search_query:
        livros = Livro.query.filter(
            Livro.titulo.ilike(f"%{search_query}%") |
            Livro.autor.ilike(f"%{search_query}%") |
            Livro.categoria.ilike(f"%{search_query}%")
        ).all()
    else:
        livros = Livro.query.all()

    return render_template("lista.html", lista_de_livros=livros)

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

@app.route("/novo")
def novo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("novo.html", titulo="Novo Livro")

@app.route("/criar", methods=["POST"])
def criar():
    if "user_id" not in session:
        return redirect(url_for("login"))

    titulo = request.form["titulo"]
    autor = request.form["autor"]
    categoria = request.form["categoria"]
    ano = request.form["ano"]
    editora = request.form["editora"]

    livro = Livro(
        titulo=titulo,
        autor=autor,
        categoria=categoria,
        ano=ano,
        editora=editora
    )

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for("inicio"))

# ===============================
# Rotas de Manipulação de Livros
# ===============================

@app.route("/deletar/<int:id>")
def deletar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    livro = Livro.query.get(id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
    return redirect(url_for("inicio"))

# ===============================
# Rotas de Reserva de Livros
# ===============================

@app.route("/reservar/<int:id>")
def reservar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    livro = Livro.query.get(id)
    if livro:
        livro.reservado = not livro.reservado
        db.session.commit()
    return redirect(url_for("inicio"))

# ===============================
# Rotas de Edição de Livros
# ===============================

@app.route("/editar/<int:id>")
def editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    livro = Livro.query.get(id)
    if livro:
        return render_template("editar.html", livro=livro)
    return redirect(url_for("inicio"))

@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    livro = Livro.query.get(id)
    if livro:
        livro.titulo = request.form["titulo"]
        livro.autor = request.form["autor"]
        livro.categoria = request.form["categoria"]
        livro.ano = request.form["ano"]
        livro.editora = request.form["editora"]
        db.session.commit()
    return redirect(url_for("inicio"))

# ===============================
# Execução da Aplicação
# ===============================

if __name__ == "__main__":
    init_db()
    create_test_user()  # Adiciona um usuário de teste ao banco de dados
    app.run(debug=True)