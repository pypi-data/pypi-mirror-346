"""Script para fazer backup dos documentos do MongoDB."""

import json
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional

from pymongo import MongoClient
from rich.console import Console
from rich.progress import Progress

console = Console()


async def backup_command(
    host: str = "localhost",
    port: int = 27017,
    database: str = "default",
    output: str = "backups",
    username: Optional[str] = None,
    password: Optional[str] = None,
    replicaset: Optional[str] = None,
    version: Optional[str] = None,
) -> None:
    """Gera backup dos documentos do MongoDB."""
    output_dir = Path(output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Gera nome do arquivo de backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_label = f"_{version}" if version else ""
    backup_file = output_dir / f"backup_{timestamp}{version_label}.tar.gz"

    uri_params = []
    if replicaset:
        uri_params.extend([f"replicaSet={replicaset}", "directConnection=false", "retryWrites=true", "w=majority"])

    uri_suffix = f"?{'&'.join(uri_params)}" if uri_params else ""

    if username and password:
        uri = f"mongodb://{username}:{password}@{host}:{port}/admin{uri_suffix}"
    else:
        uri = f"mongodb://{host}:{port}{uri_suffix}"

    client = MongoClient(
        uri, serverSelectionTimeoutMS=30000, connectTimeoutMS=20000, socketTimeoutMS=20000, maxPoolSize=1
    )
    db = client[database]
    collection = db["MetaObjects"]

    # Cria diretório temporário
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Busca todos os documentos
        documents = list(collection.find({"type": {"$in": ["composite", "document"]}}))

        with Progress() as progress:
            task = progress.add_task("[cyan]Gerando backup...", total=len(documents))

            # Processa cada documento
            for doc in documents:
                doc_path = temp_path / doc["name"]
                doc_path.mkdir(parents=True, exist_ok=True)

                # Salva documento principal
                doc_file = doc_path / "document.json"
                doc_file.write_text(json.dumps(doc, indent=2))

                # Busca documentos relacionados
                related = list(collection.find({"document": doc["name"]}))

                for rel in related:
                    rel_type = rel["type"]
                    type_path = doc_path / rel_type
                    type_path.mkdir(exist_ok=True)

                    rel_file = type_path / f"{rel['name']}.json"
                    rel_file.write_text(json.dumps(rel, indent=2))

                progress.update(task, advance=1)

        # Cria arquivo tar.gz
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(temp_dir, arcname="metadata")

    client.close()
    console.print(f"[green]Backup concluído com sucesso:[/green] [cyan]{backup_file}[/cyan]")


def main():
    """Função principal para execução via linha de comando."""
    import argparse
    import asyncio
    import sys

    parser = argparse.ArgumentParser(description="Gera backup dos documentos do MongoDB")
    parser.add_argument("--host", default="localhost", help="Host do MongoDB")
    parser.add_argument("--port", type=int, default=27017, help="Porta do MongoDB")
    parser.add_argument("--database", required=True, help="Nome do banco de dados")
    parser.add_argument("--output", default="backups", help="Diretório para salvar o backup")
    parser.add_argument("--username", help="Usuário do MongoDB")
    parser.add_argument("--password", help="Senha do MongoDB")
    parser.add_argument("--replicaset", help="Nome do ReplicaSet do MongoDB (ex: rs0)")
    parser.add_argument("--version", help="Rótulo de versão para o arquivo de backup")

    args = parser.parse_args()

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(
        backup_command(
            host=args.host,
            port=args.port,
            database=args.database,
            output=args.output,
            username=args.username,
            password=args.password,
            replicaset=args.replicaset,
            version=args.version,
        )
    )


if __name__ == "__main__":
    main()
