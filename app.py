from flask import Flask, request, jsonify
# from flask_cors import CORS
import mysql.connector
import re

app = Flask(__name__)
# CORS(app)  # Permite requisições de qualquer origem

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Returns:
        mysql.connector.connection_cext.CMySQLConnection: Conexão com o banco de dados.
    """
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='KUr52Vrkr7%5e%x6WUVB',  # Substitua pelo seu password
        database='api_database'  # Substitua pelo nome do seu banco de dados
    )
    return conn

class Validador:
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida se o email está no formato correto.

        :param email: Email a ser validado.
        :return: True se o email for válido, False caso contrário.
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """
        Valida se o telefone está no formato correto.

        :param telefone: Telefone a ser validado.
        :return: True se o telefone for válido, False caso contrário.
        """
        padrao = r'^\+?\d[\d\s-]{7,15}$'
        return re.match(padrao, telefone) is not None

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    """
    Cria um novo usuário na tabela 'usuarios' com os dados fornecidos.

    Request Body (JSON):
        - nome (str): Nome do usuário.
        - email (str): Email do usuário.
        - numero (str): Número de telefone do usuário.

    Returns:
        dict: Mensagem indicando sucesso na criação do usuário.
        int: Código de status HTTP 201 (Created).
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    numero = data.get('numero')
    
    # Verifica se o e-mail e o número são válidos
    if not Validador.validar_email(email):
        return jsonify({'message': 'Email inválido'}), 400
    if not Validador.validar_telefone(numero):
        return jsonify({'message': 'Número de telefone inválido'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, email, numero) VALUES (%s, %s, %s)', (nome, email, numero))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Obtém todos os usuários da tabela 'usuarios'.

    Returns:
        list: Lista de usuários, cada um representado como um dicionário com campos 'id', 'nome', 'email' e 'numero'.
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
        - numero (str): Novo número de telefone do usuário (opcional).

    Returns:
        dict: Mensagem indicando sucesso na atualização do usuário.
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    numero = data.get('numero')
    
    if email and not Validador.validar_email(email):
        return jsonify({'message': 'Email inválido'}), 400
    if numero and not Validador.validar_telefone(numero):
        return jsonify({'message': 'Número de telefone inválido'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nome = %s, email = %s, numero = %s WHERE id = %s', (nome, email, numero, id))
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