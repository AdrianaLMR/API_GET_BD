from flask import Flask, request, jsonify
import mysql.connector
#import re
from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # Permite todas as origens
def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: Conexão com o banco de dados.
    """
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',  # Substitua pelo seu password
        database='api_database'  # Substitua pelo nome do seu banco de dados
    )
    return conn


@app.route('/usuarios', methods=['POST'])
def create_usuario():
    """
    Cria um novo usuário na tabela 'usuarios' com os dados fornecidos.

    Request Body (JSON):
        - nome (str): Nome do usuário.
        - email (str): Email do usuário.
        - telefone (str): Número de telefone do usuário.

    Returns:
        dict: Mensagem indicando sucesso na criação do usuário.
        int: Código de status HTTP 201 (Created).
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email, telefone) VALUES (%s, %s, %s)', (nome, email, telefone))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Obtém todos os usuários da tabela 'usuarios'.

    Returns:
        list: Lista de usuários, cada um representado como um dicionário com campos 'id', 'nome', 'email' e 'telefone'.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(usuarios)

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    """
    Obtém um usuário específico da tabela 'usuarios' pelo ID fornecido.

    Args:
        id (int): ID do usuário a ser obtido.

    Returns:
        dict: Dados do usuário, ou mensagem de erro se o usuário não for encontrado.
        int: Código de status HTTP 404 (Not Found) se o usuário não for encontrado.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario is None:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    return jsonify(usuario)

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    """
    Atualiza os dados de um usuário específico na tabela 'usuarios' pelo ID fornecido.

    Args:
        id (int): ID do usuário a ser atualizado.

    Request Body (JSON):
        - nome (str): Novo nome do usuário (opcional).
        - email (str): Novo email do usuário (opcional).
        - telefone (str): Novo número de telefone do usuário (opcional).

    Returns:
        dict: Mensagem indicando sucesso na atualização do usuário.
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nome = %s, email = %s, telefone = %s WHERE id = %s', (nome, email, telefone, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Usuário atualizado com sucesso!'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    """
    Deleta um usuário específico da tabela 'usuarios' pelo ID fornecido.

    Args:
        id (int): ID do usuário a ser deletado.

    Returns:
        dict: Mensagem indicando sucesso na exclusão do usuário.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Usuário deletado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)