document.addEventListener('DOMContentLoaded', () => {
    fetchUsuarios();

    document.getElementById('usuario-form').addEventListener('submit', (e) => {
        e.preventDefault();
        adicionarUsuario();
    });
    ;


    document.getElementById('edit-form').addEventListener('submit', (e) => {
        e.preventDefault();
        editarUsuario();
    });

    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('edit-modal').style.display = 'none';
    });
});

async function fetchUsuarios() {
    const response = await fetch('http://localhost:5000/usuarios');
    const usuarios = await response.json();
    const tbody = document.querySelector('#usuarios-table tbody');
    tbody.innerHTML = '';
    usuarios.forEach(usuario => {
        tbody.innerHTML += `
            <tr>
                <td>${usuario.id}</td>
                <td>${usuario.nome}</td>
                <td>${usuario.email}</td>
                <td>${usuario.telefone}</td>
                <td>
                    <button onclick="mostrarEditarModal(${usuario.id}, '${usuario.nome}', '${usuario.email}', '${usuario.telefone}')">Editar</button>
                    <button onclick="deletarUsuario(${usuario.id})">Excluir</button>
                </td>
            </tr>`;
    });
}

async function adicionarUsuario() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value;

    const response = await fetch('http://localhost:5000/usuarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email, telefone })
    });
    const data = await response.json();
    alert(data.message);
    fetchUsuarios();

    // Limpa os campos após adicionar o usuário
    document.getElementById('usuario-form').reset();
}

async function editarUsuario() {
    const id = document.getElementById('edit-id').value;
    const nome = document.getElementById('edit-nome').value;
    const email = document.getElementById('edit-email').value;
    const telefone = document.getElementById('edit-telefone').value;

    const response = await fetch(`http://localhost:5000/usuarios/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email, telefone })
    });
    const data = await response.json();
    alert(data.message);
    document.getElementById('edit-modal').style.display = 'none';
    fetchUsuarios();

    // Limpa os campos após editar o usuário
    document.getElementById('edit-form').reset();
}

async function deletarUsuario(id) {
    const response = await fetch(`http://localhost:5000/usuarios/${id}`, { method: 'DELETE' });
    const data = await response.json();
    alert(data.message);
    fetchUsuarios();
}

function mostrarEditarModal(id, nome, email, telefone) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-nome').value = nome;
    document.getElementById('edit-email').value = email;
    document.getElementById('edit-telefone').value = telefone;
    document.getElementById('edit-modal').style.display = 'block';
}
