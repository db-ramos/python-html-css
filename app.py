import sqlite3
from flask import Flask, g, render_template

DATABASE = "blog.db"
SECRET_KEY = "pudim"

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(DATABASE)

@app.before_request
def pre_requisicao():
    g.bd = conectar_bd()

@app.teardown_request
def pos_requisicao(exception):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall():
        entradas.append({'titulo': titulo, 'texto': texto})
    return render_template('exibir_entradas.html', entradas=entradas)
