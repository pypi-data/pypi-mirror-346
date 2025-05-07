"""Script para extrair dados do MongoDB e gerar arquivos JSON."""

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union, cast

import black
import inquirer
from pymongo import MongoClient
from rich.console import Console
from rich.progress import Progress
from rich.table import Table


class DocFiles(TypedDict):
    document: List[Path]
    view: List[Path]
    list: List[Path]
    pivot: List[Path]
    access: List[Path]
    hook: List[Path]


class RelatedResults(TypedDict):
    view: List[str]
    list: List[str]
    pivot: List[str]
    access: List[str]


class MongoFilter(TypedDict, total=False):
    document: str
    type: str
    name: str
    or_conditions: List[Dict[str, str]]


class MongoCondition(TypedDict, total=False):
    type: str
    name: str


MongoQuery = Dict[str, Union[str, List[MongoCondition]]]


DocType = Literal["document", "view", "list", "pivot", "access", "hook"]
MetaType = Literal["view", "list", "pivot", "access"]


console = Console()


def format_code(name: str, code: str) -> str:
    """Formata o código JavaScript usando black."""
    try:
        return black.format_str(code, mode=black.Mode())
    except Exception as error:
        console.print(f"[red]Erro ao formatar código {name}[/red]: {str(error)}")
        return code


async def write_file(file_path: str, content: str) -> None:
    """Escreve conteúdo em um arquivo, criando diretórios se necessário."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    except Exception as error:
        console.print(f"[red]Erro ao escrever arquivo {file_path}[/red]: {str(error)}")


async def pull_command(
    doc_parameter: Optional[str] = None,
    host: str = "localhost",
    port: int = 27017,
    database: str = "default",
    output: str = "metadata",
    view: Optional[str] = None,
    list_param: Optional[str] = None,
    pivot: Optional[str] = None,
    access: Optional[str] = None,
    hook: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    replicaset: Optional[str] = None,
    extract_all: bool = False,
) -> None:
    """Extrai dados do MongoDB e gera arquivos JSON."""
    output_dir = Path(output).resolve()

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

    document = doc_parameter

    table = Table(title="Resultados da Extração")
    table.add_column("Documento")
    table.add_column("Hook")
    table.add_column("View")
    table.add_column("List")
    table.add_column("Pivot")
    table.add_column("Access")

    if document is None and not extract_all:
        document_names = list(
            collection.find({"type": {"$in": ["composite", "document"]}}, {"name": 1}).sort("name", 1)
        )
        choices = [{"name": "Todos", "value": "all"}] + [
            {"name": doc["name"], "value": doc["name"]} for doc in document_names
        ]

        questions = [
            inquirer.List(
                "document", message="Qual documento você precisa?", choices=[choice["name"] for choice in choices]
            )
        ]
        answers = inquirer.prompt(questions)
        if answers is None:
            console.print("[red]Operação cancelada pelo usuário[/red]")
            return
        document = "all" if answers["document"] == "Todos" else answers["document"]
    elif extract_all:
        document = "all"

    filter_query: Dict[str, Any] = {"type": {"$in": ["composite", "document"]}}
    if document != "all":
        filter_query["name"] = document

    metas = list(collection.find(filter_query).sort("_id", 1))

    with Progress() as progress:
        task = progress.add_task("[cyan]Processando...", total=len(metas))

        for doc in metas:
            doc_path = output_dir / doc["name"]

            # Processando hooks
            hook_results = []
            if hook or all(x is None for x in [view, list_param, pivot, access]):
                doc_meta = doc.copy()
                for field in ["scriptBeforeValidation", "validationData", "validationScript", "scriptAfterSave"]:
                    doc_meta.pop(field, None)

                if hook in (None, "validationData") and "validationData" in doc:
                    await write_file(
                        str(doc_path / "hook" / "validationData.json"), json.dumps(doc["validationData"], indent=2)
                    )
                    hook_results.append("✓ validationData")

                for script_type in ["scriptBeforeValidation", "validationScript", "scriptAfterSave"]:
                    if script_type in doc and (hook is None or hook == script_type):
                        formatted = format_code(f"{script_type}.js", doc[script_type])
                        await write_file(str(doc_path / "hook" / f"{script_type}.js"), formatted)
                        hook_results.append(f"✓ {script_type}")

                if hook is None:
                    await write_file(str(doc_path / "document.json"), json.dumps(doc_meta, indent=2))

            # Processando views, lists, pivots e access
            related_results: RelatedResults = {"view": [], "list": [], "pivot": [], "access": []}
            if all(x is None for x in [hook, view, list_param, pivot, access]) or any(
                x is not None for x in [view, list_param, pivot, access]
            ):
                MONGO_OR = "$or"
                meta_filter = {"document": doc["name"]}
                meta_filter[MONGO_OR] = []

                if any(x is not None for x in [view, list_param, pivot, access]):
                    for type_name, param in [
                        ("view", view),
                        ("list", list_param),
                        ("pivot", pivot),
                        ("access", access),
                    ]:
                        if param is not None:
                            condition = {"type": type_name}
                            if param != "all":
                                condition["name"] = param
                            meta_filter[MONGO_OR].append(condition)

                related_metas = list(collection.find(meta_filter).sort("_id", 1))

                for meta in related_metas:
                    meta_type = cast(MetaType, meta["type"])
                    if meta_type in ("view", "list", "pivot", "access"):
                        await write_file(str(doc_path / meta_type / f"{meta['name']}.json"), json.dumps(meta, indent=2))
                        related_results[meta_type].append(f"✓ {meta['name']}")

            table.add_row(
                doc["name"],
                "\n".join(hook_results),
                "\n".join(related_results["view"]),
                "\n".join(related_results["list"]),
                "\n".join(related_results["pivot"]),
                "\n".join(related_results["access"]),
            )

            progress.update(task, advance=1)

    client.close()
    console.print(f"[green]Extração concluída com sucesso do banco[/green] [cyan]{database}[/cyan]")
    if document != "all":
        console.print(f"[cyan]Documento: {document}[/cyan]")

    console.print(table)


def main():
    """Função principal para execução via linha de comando."""
    import argparse
    import asyncio
    import sys

    parser = argparse.ArgumentParser(description="Extrai dados do MongoDB")
    parser.add_argument("--host", default="localhost", help="Host do MongoDB")
    parser.add_argument("--port", type=int, default=27017, help="Porta do MongoDB")
    parser.add_argument("--database", required=True, help="Nome do banco de dados")
    parser.add_argument("--output", default="metadata", help="Diretório de saída")
    parser.add_argument("--view", help="Nome da view específica para extrair")
    parser.add_argument("--list", dest="list_param", help="Nome da lista específica para extrair")
    parser.add_argument("--pivot", help="Nome do pivot específico para extrair")
    parser.add_argument("--access", help="Nome do access específica para extrair")
    parser.add_argument("--hook", help="Nome do hook específico para extrair")
    parser.add_argument("--username", help="Usuário do MongoDB")
    parser.add_argument("--password", help="Senha do MongoDB")
    parser.add_argument("--replicaset", help="Nome do ReplicaSet do MongoDB (ex: rs0)")
    parser.add_argument("collection", nargs="?", help="Nome da collection específica para extrair")
    parser.add_argument("--all", action="store_true", help="Extrair todas as collections sem perguntar")

    args = parser.parse_args()
    args_dict = vars(args)

    # Se collection foi especificada, usa como doc_parameter
    if "collection" in args_dict:
        args_dict["doc_parameter"] = args_dict.pop("collection")

    # Renomeia o parâmetro all para extract_all
    if "all" in args_dict:
        args_dict["extract_all"] = args_dict.pop("all")

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(pull_command(**args_dict))


if __name__ == "__main__":
    main()
