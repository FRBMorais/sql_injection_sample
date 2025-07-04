from flask import Flask, request, render_template
import sqlite3
import time

app = Flask(__name__)

# Conecta ao banco e cria tabela
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nome TEXT
        )
    ''')
    c.execute("INSERT INTO users (nome) VALUES ('Estudante Felipe')")
    c.execute("INSERT INTO users (nome) VALUES ('Professor Felipe')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ''
    if request.method == 'POST':
        id = request.form['id']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        query = f"SELECT nome FROM users WHERE id = {id}"  # vulnerabilidade
        try:
            start = time.time()
            c.execute(query)
            rows = c.fetchall()
            end = time.time()
            if rows:
                resultado = f"Nome: {rows[0][0]} | Tempo consulta: {round(end-start,2)}s"
            else:
                resultado = f"Nenhum usuário encontrado | Tempo consulta: {round(end-start,2)}s"
        except Exception as e:
            resultado = f"Erro: {e}"
        conn.close()
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
