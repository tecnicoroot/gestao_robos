import logging
from datetime import datetime
from pathlib import Path


def configurar_logging(
    diretorio: str | Path = "logs",
    nome_arquivo: str = "validador_tiss",
) -> None:
    """
    Configura o sistema de logging da aplicação.
    """

    diretorio = Path(diretorio)
    diretorio.mkdir(parents=True, exist_ok=True)

    data = datetime.now().strftime("%Y%m%d_%H%M%S")

    arquivo_log = diretorio / f"{nome_arquivo}_{data}.log"

    formato = "%(asctime)s [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s"

    logging.basicConfig(
        level=logging.DEBUG,
        format=formato,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(
                arquivo_log,
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )
