from compressbench.compressors.base import Compressor
from compressbench.types import BenchmarkResult


def run_benchmarks(input_file: str, compressors: list[Compressor]) -> list[BenchmarkResult]:
    return [compressor.benchmark(input_file) for compressor in compressors]
