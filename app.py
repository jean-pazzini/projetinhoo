import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tarefas.db"))

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --- MODELO (A tabela do banco) ---
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pendente')

# --- CORREÇÃO AQUI ---
# Movemos a criação do banco para cá, fora do "if __name__"
# Assim, o Gunicorn executa isso antes de receber o primeiro acesso.
with app.app_context():
    db.create_all()

# --- ROTAS ---
@app.route("/")
def index():
    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas)