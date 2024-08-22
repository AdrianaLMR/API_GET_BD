from flask import Flask, jsonify
import mysql.connector

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

def get_db_connection():
    """
    Estabelece e retorna uma conexão com o banco de dados MySQL.
    
    :return: Conexão com o banco de dados
    """
    conn = mysql.connector.connect(
        host='localhost',          # Endereço do servidor MySQL
        user='root',               # Nome de usuário para conectar ao MySQL
        password='KUr52Vrkr7%5e%x6WUVB',  # Senha do usuário do MySQL
        database='api_database'    # Nome do banco de dados a ser usado
    )
    return conn

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Manipulador de rota para a URL '/usuarios'.
    
    Conecta ao banco de dados, executa uma consulta para obter todos os registros da tabela 'usuarios',
    e retorna esses registros como uma resposta JSON.
    
    :return: Resposta JSON contendo a lista de usuários
    """
    # Obtém uma conexão com o banco de dados
    conn = get_db_connection()
    
    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor(dictionary=True)
    
    # Executa a consulta SQL para obter todos os registros da tabela 'usuarios'
    cursor.execute('SELECT * FROM usuarios')
    
    # Recupera todos os resultados da consulta
    usuarios = cursor.fetchall()
    
    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    conn.close()
    
    # Retorna os resultados como uma resposta JSON
    return jsonify(usuarios)

if __name__ == '__main__':
    """
    Executa o aplicativo Flask em modo de depuração.
    
    Quando executado diretamente, inicia o servidor de desenvolvimento Flask.
    """
    app.run(debug=True)
