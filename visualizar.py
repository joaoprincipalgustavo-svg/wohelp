import sqlite3

def visualizar_cadastros():
    try:
        # Conecta ao banco de dados wohelp.db
        conn = sqlite3.connect('wohelp.db')
        cursor = conn.cursor()

        # Busca todos os dados da tabela ALUNOS (corrigido aqui!)
        cursor.execute("SELECT id, nome, idade, aspiracao, universidade FROM alunos")
        mulheres_cadastradas = cursor.fetchall()

        # Verifica se a lista está vazia
        if not mulheres_cadastradas:
            print("📭 O banco de dados está vazio. Nenhuma jornada iniciada ainda.")
        else:
            print("\n🌸 --- REDE DE APOIO WOHELP : CADASTRADAS --- 🌸\n")
            
            # Repete para cada mulher encontrada no banco
            for mulher in mulheres_cadastradas:
                id_usuario, nome, idade, aspiracao, universidade = mulher
                
                # Trata o campo universidade caso a pessoa tenha deixado em branco
                local_estudo = universidade if universidade else "Não preenchido"

                print(f"🔸 ID: {id_usuario}")
                print(f"   Nome: {nome}")
                print(f"   Idade: {idade} anos")
                print(f"   Objetivo/Aspiração: {aspiracao}")
                print(f"   Estudo: {local_estudo}")
                print("-" * 45)

    except sqlite3.OperationalError:
        print("⚠️ Erro: O banco de dados ou a tabela ainda não existem.")
        print("Rode o 'app.py' e faça pelo menos um cadastro primeiro!")
        
    finally:
        # Garante que a conexão com o banco seja fechada no final
        if 'conn' in locals():
            conn.close()


def main():
    print("Olá, você está no visualizar, escolhe uma função, 1 para ver, dois para apagar os dados")
    k = int(input("Escolha uma opçao: "))
    if k != 1 and k != 2:
     print("ERRO, ESCOLHA UM OU DOIS")
    elif k == 1:
     visualizar_cadastros()
     main()
    else:
     print("Deletando todos os cadastros...")

     conn = sqlite3.connect('wohelp.db')
     cursor = conn.cursor()

     cursor.execute("DELETE FROM alunos")

     conn.commit()
     conn.close()

     print("Todos os cadastros foram deletados!")

if __name__ == "__main__":
    main()