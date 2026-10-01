import logging
from pathlib import Path

from gestao_robos.config.logging_config import configurar_logging


def test_configurar_logging_cria_diretorio(tmp_path: Path) -> None:
    diretorio = tmp_path / "logs"

    configurar_logging(
        diretorio=diretorio,
        nome_arquivo="teste",
    )

    assert diretorio.exists()
    assert diretorio.is_dir()


def test_configurar_logging_cria_arquivo(tmp_path: Path) -> None:
    configurar_logging(
        diretorio=tmp_path,
        nome_arquivo="teste",
    )

    arquivos = list(tmp_path.glob("teste_*.log"))

    assert len(arquivos) == 1


def test_configurar_logging_grava_mensagem(tmp_path: Path) -> None:
    configurar_logging(
        diretorio=tmp_path,
        nome_arquivo="teste",
    )

    logger = logging.getLogger("teste")

    logger.info("Mensagem de teste")

    arquivos = list(tmp_path.glob("teste_*.log"))

    assert len(arquivos) == 1

    conteudo = arquivos[0].read_text(encoding="utf-8")

    assert "Mensagem de teste" in conteudo
