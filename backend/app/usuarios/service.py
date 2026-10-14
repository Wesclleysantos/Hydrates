from pwdlib import PasswordHash
from app.usuarios import repository

password_hash = PasswordHash.recommended()

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)

def autenticar_usuario(email: str, senha: str):
    email = email.strip().lower()
    usuario = repository.buscar_por_email(email)

    if not usuario:
        return None

    senha_correta = verificar_senha(
        senha,
        usuario["senha_hash"],
    )

    if not senha_correta:
        return None

    return usuario

def cadastrar_usuario(
    nome: str,
    email: str,
    senha: str,
    peso: float | None = None,
    idade: int | None = None,
):
    nome = nome.strip()
    email = email.strip().lower()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not email or "@" not in email:
        raise ValueError("Informe um e-nail válido.")

    if len(senha) < 8:
        raise ValueError("A senha deve ter pelo menos 8 caracteres.")

    if peso is not None and peso <= 0:
        raise ValueError("O peso deve ser maior que zero.")

    if idade is not None and idade <= 0:
        raise ValueError("A idade deve ser maior que zero.")

    usuario_existente = repository.buscar_por_email(email)

    if usuario_existente:
        raise ValueError("Este e-mail já está cadastrado.")

    senha_hash = password_hash.hash(senha)

    usuario_id = repository.criar_usuario(
        nome = nome,
        email = email,
        senha_hash = senha_hash,
        peso = peso,
        idade = idade,
    )

    return {
        "id": usuario_id,
        "nome": nome,
        "email": email,
        "peso": peso,
        "idade": idade,
        "pontos": 0,
    }
