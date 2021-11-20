import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session

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
    return render_template("exibir_entradas.html", entradas=entradas)

#Esta rota receberá os dados do formulário de "templates/exibir_entradas.html"
# methods=["POST"] -> configura a rota para receber requisições de formulários HTML com método POST (<form method=POST>)
@app.route('/inserir', methods=["POST"])
def inserir_entrada():
    titulo = request.form['titulo']
    texto = request.form['texto']
    sql = "insert INTO entradas(titulo,texto) values (?,?)"
    g.bd.execute(sql,[titulo,texto])
    g.bd.commit()
    flash("Postagem registrada. Valeu!!")
    return redirect(url_for('exibir_entradas'))

@app.route('/login',methods=['GET','POST'])
def login():
    erro = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form['password'] != "admin":
            erro = "Usuário ou senha inválidos"
        else:
            session['logado'] = True
            flash("Login efetuado com sucesso")
            return redirect(url_for('exibir_entradas'))
    return render_template('login.html', erro=erro)

@app.route("/logout")
def logout():
    session.pop("logado",None)
    flash("Volte sempre!!")
    return redirect(url_for("exibir_entradas"))