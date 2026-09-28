from dataclasses import dataclass
from datetime import time


@dataclass
class Robot:
    """Representa um robô cadastrado na tabela `robos`."""

    id: int | None
    nome: str
    descricao: str
    ativo: bool
    intervalo: int
    acao: str
    tela: str
    path_executavel: str
    limite_tempo: int
    arquivo_ativacao: str
    nome_executavel: str
    pasta_trabalho: str
    repositorio_planilhas: str
    notificados: str
    pgm_ativado1: str
    pgm_ativado2: str
    robo_sequencia: int
    usuario_robo: str
    robo_teste: int
    horario_ativacao: time
    codigo_setor: int
    biblioteca: str

    def __post_init__(self) -> None:
        """Valida e normaliza os dados do robô."""

        self.nome = self.nome.strip()
        self.descricao = self.descricao.strip()
        self.acao = self.acao.strip()
        self.tela = self.tela.strip()
        self.path_executavel = self.path_executavel.strip()
        self.arquivo_ativacao = self.arquivo_ativacao.strip()
        self.nome_executavel = self.nome_executavel.strip()
        self.pasta_trabalho = self.pasta_trabalho.strip()
        self.repositorio_planilhas = self.repositorio_planilhas.strip()
        self.notificados = self.notificados.strip()
        self.pgm_ativado1 = self.pgm_ativado1.strip()
        self.pgm_ativado2 = self.pgm_ativado2.strip()
        self.usuario_robo = self.usuario_robo.strip()
        self.biblioteca = self.biblioteca.strip()

        if not self.nome:
            raise ValueError("O nome do robô é obrigatório.")

    def activate(self) -> None:
        """Ativa o robô."""

        self.ativo = True

    def deactivate(self) -> None:
        """Desativa o robô."""

        self.ativo = False

    def update(
        self,
        nome: str,
        descricao: str,
    ) -> None:
        """Atualiza nome e descrição do robô."""

        nome = nome.strip()
        descricao = descricao.strip()

        if not nome:
            raise ValueError("O nome do robô é obrigatório.")

        self.nome = nome
        self.descricao = descricao
