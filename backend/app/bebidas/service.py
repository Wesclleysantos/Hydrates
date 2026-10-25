from app.bebidas import repository

def listar_bebidas(usuario_id: int):
    return repository.listar_bebidas(usuario_id=usuario_id)

def cadastrar_bebida(
    usuario_id: int,
    nome: str,
    fator_hidratacao: float,
):
    nome = nome.strip()

    if not nome:
        raise ValueError("O nome da bebida é obrigatório.")

    if not 0 < fator_hidratacao <= 1:
        raise ValueError(
            "O fator de hidratação deve ser maior que 0 e menor ou igual a 1."
        )

    bebida_existente = repository.buscar_por_nome(
        nome=nome,
        usuario_id=usuario_id,
    )

    if bebida_existente:
        raise ValueError("Você já cadastrou uma bebida com esse nome.")

    return repository.criar_bebida(
        usuario_id=usuario_id,
        nome=nome,
        fator_hidratacao=fator_hidratacao,
    )

def atualizar_bebida(
    usuario_id: int,
    bebida_id: int,
    nome: str,
    fator_hidratacao: float,
):
    nome = nome.strip()

    if not nome:
        raise ValueError("O nome da bebida é obrigatório.")

    if not 0 < fator_hidratacao <= 1:
        raise ValueError(
            "O fator de hidratação deve ser maior que 0 e menor ou igual a 1."
        )

    bebida = repository.buscar_bebida_do_usuario(
        bebida_id=bebida_id,
        usuario_id=usuario_id,
    )

    if not bebida:
        raise LookupError("Bebida não encontrada para este usuário.")

    bebida_existente = repository.buscar_por_nome(
        nome=nome,
        usuario_id=usuario_id,
        excluir_bebida_id=bebida_id,
    )

    if bebida_existente:
        raise ValueError("Você já cadastrou uma bebida com esse nome.")

    repository.atualizar_bebida_do_usuario(
        bebida_id=bebida_id,
        usuario_id=usuario_id,
        nome=nome,
        fator_hidratacao=fator_hidratacao,
    )
    