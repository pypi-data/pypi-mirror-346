from pathlib import Path

import typer

from compressbench import __version__
from compressbench.benchmark import run_benchmarks
from compressbench.compressors.gzip import GzipCompressor
from compressbench.compressors.snappy import SnappyCompressor
from compressbench.results import output_results

app = typer.Typer(
    help="Benchmark compression algorithms on Parquet datasets.",
)

ALGORITHM_MAP = {
    "gzip": GzipCompressor,
    "snappy": SnappyCompressor,
}


@app.command()
def benchmark(
    input_file: str = typer.Argument(..., help="Path to the Parquet file to benchmark."),
    algorithms: list[str] = typer.Option(
        None,
        "--algorithms",
        "-a",
        help="Compression algorithms to test (gzip, snappy).",
    ),
    output_format: str = typer.Option("text", "--output-format", "-o", help="Output format: text, json, csv."),
):
    """
    Run compression benchmark on the specified Parquet file.
    """
    if not Path(input_file).exists():
        typer.echo("Error: Input file does not exist.")
        raise typer.Exit(code=1)

    if not algorithms:
        algorithms = ["gzip", "snappy"]

    compressors = []
    for algo in algorithms:
        algo = algo.lower()
        if algo not in ALGORITHM_MAP:
            typer.echo(f"Error: Unsupported algorithm '{algo}'. Supported: {list(ALGORITHM_MAP.keys())}")
            raise typer.Exit(code=1)
        compressors.append(ALGORITHM_MAP[algo]())

    results = run_benchmarks(input_file, compressors)

    output_results(results, output_format)


@app.command()
def version():
    """Show the installed version."""
    print(f"compressbench version {__version__}")


if __name__ == "__main__":
    app()
