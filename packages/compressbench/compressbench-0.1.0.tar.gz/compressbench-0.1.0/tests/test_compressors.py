from pathlib import Path

import pytest

from compressbench.benchmark import run_benchmarks
from compressbench.compressors.gzip import GzipCompressor
from compressbench.compressors.snappy import SnappyCompressor
from compressbench.types import BenchmarkResult

TEST_FILE = Path("tests/data/test_data.parquet")


@pytest.fixture(scope="session")
def test_parquet_file():
    """Fixture to provide a small Parquet file for benchmarking tests."""
    if not TEST_FILE.exists():
        import pandas as pd

        df = pd.DataFrame({"col1": range(1000), "col2": ["test_string"] * 1000})
        TEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(TEST_FILE, index=False)
    return str(TEST_FILE)


def test_gzip_compression(test_parquet_file):
    """Test gzip compressor produces valid benchmark results."""
    compressor = GzipCompressor()
    results = run_benchmarks(test_parquet_file, [compressor])
    result = results[0]

    assert isinstance(result, BenchmarkResult)
    assert result.compression_ratio > 0
    assert result.compression_time > 0
    assert result.decompression_time > 0

    print("\nGzip Benchmark Result:")
    print(result)


def test_snappy_compression(test_parquet_file):
    """Test snappy compressor produces valid benchmark results."""

    compressor = SnappyCompressor()
    results = run_benchmarks(test_parquet_file, [compressor])
    result = results[0]

    assert isinstance(result, BenchmarkResult)
    assert result.compression_ratio > 0
    assert result.compression_time > 0
    assert result.decompression_time > 0

    print("\nSnappy Benchmark Result:")
    print(result)


def test_multiple_compressors(test_parquet_file):
    """Test multiple compressors return valid benchmark results."""
    compressors = [GzipCompressor(), SnappyCompressor()]
    results = run_benchmarks(test_parquet_file, compressors)

    assert len(results) == 2
    for result in results:
        assert isinstance(result, BenchmarkResult)
        assert result.compression_ratio > 0
        assert result.compression_time > 0
        assert result.decompression_time > 0

    print("\nMultiple Compressor Results:")
    for r in results:
        print(r)
