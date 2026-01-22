import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados
# Em produção, você trocaria isso por um link do PostgreSQL
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

# --- ROTAS ---

# R - READ (Ler/Listar)
@app.route("/")
def index():
    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas)

# C - CREATE (Criar)
@app.route("/adicionar", methods=["POST"])
def adicionar():
    conteudo = request.form.get("conteudo")
    if conteudo:
        nova_tarefa = Tarefa(conteudo=conteudo)
        db.session.add(nova_tarefa)
        db.session.commit()
    return redirect(url_for("index"))

# U - UPDATE (Atualizar)
@app.route("/atualizar/<int:id>")
def atualizar(id):
    tarefa = Tarefa.query.get(id)
    # Lógica simples: inverte o status
    if tarefa.status == 'Pendente':
        tarefa.status = 'Concluído'
    else:
        tarefa.status = 'Pendente'
    db.session.commit()
    return redirect(url_for("index"))

# D - DELETE (Deletar)
@app.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Tarefa.query.get(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Cria o banco de dados se não existir
    with app.app_context():
        db.create_all()
    app.run(debug=True)