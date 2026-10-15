from app.bebidas import repository

def listar_bebidas():
    return repository.listar_bebidas()

def cadastrar_bebida(nome: str, fator_hidratacao: float):
    nome = nome.strip()

    if not nome:
        raise ValueError("O nome da bebida é obrigatório.")

    if not 0 < fator_hidratacao <= 1:
        raise ValueError("O fator de hidratação deve ser maior que 0 e menor ou igual a 1.")

    bebida_existente = repository.buscar_por_nome(nome)

    if bebida_existente:
        raise ValueError("Já existe uma bebida cadastrada com esse nome.")

    return repository.criar_bebida(
        nome = nome,
        fator_hidratacao = fator_hidratacao,
    )
