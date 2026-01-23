import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- CONFIGURAÇÃO ---
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tarefas.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pendente')

# --- O PULO DO GATO: CRIAÇÃO DO BANCO ---
# Este comando PRECISA estar aqui fora, colado na margem esquerda (sem recuo/indentação).
# Assim o Render executa ele assim que liga o site.
with app.app_context():
    db.create_all()

# --- ROTAS (Também sem recuo) ---

@app.route("/")
def index():
    # O comando try/except evita que o site caia se o banco sumir
    try:
        tarefas = Tarefa.query.all()
    except:
        tarefas = []
    return render_template("index.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    conteudo = request.form.get("conteudo")
    if conteudo:
        nova_tarefa = Tarefa(conteudo=conteudo)
        db.session.add(nova_tarefa)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/atualizar/<int:id>")
def atualizar(id):
    tarefa = Tarefa.query.get(id)
    if tarefa:
        if tarefa.status == 'Pendente':
            tarefa.status = 'Concluído'
        else:
            tarefa.status = 'Pendente'
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/deletar/<int:id>")
def deletar(id):
    tarefa = Tarefa.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    return redirect(url_for("index"))

# --- APENAS PARA RODAR LOCALMENTE ---
if __name__ == "__main__":
    app.run(debug=True)