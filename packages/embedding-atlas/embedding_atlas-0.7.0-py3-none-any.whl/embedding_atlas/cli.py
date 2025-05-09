# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

"""Command line interface."""

import asyncio
import logging
import pathlib
import socket
from pathlib import Path

import click
import inquirer
import numpy as np
import pandas as pd
import uvicorn
import uvloop

from .data_source import DataSource
from .server import make_server
from .utils import Hasher, load_huggingface_data, load_pandas_data
from .version import __version__


def find_column_name(existing_names, candidate):
    if candidate not in existing_names:
        return candidate
    else:
        index = 1
        while True:
            s = f"{candidate}_{index}"
            if s not in existing_names:
                return s
            index += 1


def determine_and_load_data(filename: str, splits: list[str] | None = None):
    suffix = Path(filename).suffix.lower()
    hf_prefix = "hf://datasets/"

    # Override Hugging Face data if given full url
    if filename.startswith(hf_prefix):
        filename = filename.split(hf_prefix)[-1]

    # Hugging Face data
    if (len(filename.split("/")) <= 2) and (suffix == ""):
        df = load_huggingface_data(filename, splits)
    else:
        df = load_pandas_data(filename)

    return df


def load_datasets(
    inputs: list[str], splits: list[str] | None = None, sample: int | None = None
) -> pd.DataFrame:
    existing_column_names = set()
    dataframes = []
    for fn in inputs:
        print("Loading data from " + fn)
        df = determine_and_load_data(fn, splits=splits)
        dataframes.append(df)
        for c in df.columns:
            existing_column_names.add(c)

    file_name_column = find_column_name(existing_column_names, "FILE_NAME")
    for df, fn in zip(dataframes, inputs):
        df[file_name_column] = fn

    df = pd.concat(dataframes)

    if sample:
        df = df.sample(n=sample, axis=0, random_state=np.random.RandomState(42))

    return df


def prompt_for_column(df: pd.DataFrame, message: str) -> str | None:
    question = [
        inquirer.List(
            "arg",
            message=message,
            choices=sorted(["(none)"] + [str(c) for c in df.columns]),
        ),
    ]
    r = inquirer.prompt(question)
    if r is None:
        return None
    text = r["arg"]  # type: ignore
    if text == "(none)":
        text = None
    return text


def find_available_port(start_port: int, max_attempts: int = 10, host="localhost"):
    """Find the next available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError("No available ports found in the given range")


@click.command()
@click.argument("inputs", nargs=-1, required=True)
@click.option("--text", default=None, help="The column name for text.")
@click.option("--image", default=None, help="The column name for image.")
@click.option(
    "--split",
    default=[],
    multiple=True,
    help="The data split name for Hugging Face data. Repeat this command for multiple splits.",
)
@click.option(
    "--model",
    default=None,
    help="The model for producing text embeddings.",
)
@click.option(
    "--trust-remote-code",
    is_flag=True,
    default=False,
    help="Trust remote code when loading models.",
)
@click.option("--x", "x_column", help="The column name for x coordinate.")
@click.option("--y", "y_column", help="The column name for y coordinate.")
@click.option(
    "--neighbors",
    "neighbors_column",
    help="""The column name for pre-computed nearest neighbors. The values should be in {"ids": [n1, n2, ...], "distances": [d1, d2, ...]} format.""",
)
@click.option(
    "--sample",
    default=None,
    type=int,
    help="The number of rows to sample from the original dataset.",
)
@click.option(
    "--umap-n-neighbors",
    type=int,
    help="The n_neighbors parameter for UMAP.",
)
@click.option(
    "--umap-min-dist",
    type=float,
    help="The min_dist parameter for UMAP.",
)
@click.option("--umap-metric", default="cosine", help="The metric for UMAP.")
@click.option("--umap-random-state", type=int, help="The random seed for UMAP.")
@click.option(
    "--duckdb",
    type=str,
    default="wasm",
    help="DuckDB server URI (e.g., ws://localhost:3000, http://localhost:3000), or 'wasm' to run DuckDB in browser, or 'server' to run DuckDB in this server. Default to 'wasm'.",
)
@click.option("--host", default="localhost", help="The hostname of the http server.")
@click.option("--port", default=5055, help="The port of the http server.")
@click.option(
    "--auto-port/--no-auto-port",
    "enable_auto_port",
    default=True,
    help="Enable / disable auto port selection. If disabled, the application crashes if the specified port is already used.",
)
@click.option("--static", type=str, help="Path to the static files for frontend.")
@click.option(
    "--export-application",
    type=str,
    help="Export a static Web application to the given zip file and exit.",
)
@click.version_option(version=__version__, package_name="embedding_atlas")
def main(
    inputs,
    text: str | None,
    image: str | None,
    split: list[str] | None,
    model: str | None,
    trust_remote_code: bool,
    x_column: str | None,
    y_column: str | None,
    neighbors_column: str | None,
    sample: int | None,
    umap_n_neighbors: int | None,
    umap_min_dist: int | None,
    umap_metric: str | None,
    umap_random_state: int | None,
    static: str | None,
    duckdb: str,
    host: str,
    port: int,
    enable_auto_port: bool,
    export_application: str | None,
):
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: (%(name)s) %(message)s",
    )

    df = load_datasets(inputs, splits=split, sample=sample)

    print(df)

    id_column = find_column_name(df.columns, "_row_index")
    df[id_column] = range(df.shape[0])

    metadata = {
        "columns": {
            "id": id_column,
            "text": text,
        },
    }

    if x_column is not None and y_column is not None:
        metadata["columns"]["embedding"] = {
            "x": x_column,
            "y": y_column,
        }
    if neighbors_column is not None:
        metadata["columns"]["neighbors"] = neighbors_column

    hasher = Hasher()
    hasher.update(inputs)
    hasher.update(metadata)
    identifier = hasher.hexdigest()

    dataset = DataSource(identifier, df, metadata)

    if static is None:
        static = str((pathlib.Path(__file__).parent / "static").resolve())

    if export_application is not None:
        with open(export_application, "wb") as f:
            f.write(dataset.make_archive(static))
        exit(0)

    app = make_server(dataset, static_path=static, duckdb_uri=duckdb)

    if enable_auto_port:
        new_port = find_available_port(port, max_attempts=10, host=host)
        if new_port != port:
            logging.info(f"Port {port} is not available, using {new_port}")
    else:
        new_port = port
    uvicorn.run(app, port=new_port, host=host, loop="uvloop", access_log=False)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    main()
