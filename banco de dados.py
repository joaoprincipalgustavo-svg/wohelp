import sqlite3

conexao = sqlite3.connect("wohelp.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    aspiracao TEXT,
    universidade TEXT
)
""")

conexao.commit()
conexao.close()