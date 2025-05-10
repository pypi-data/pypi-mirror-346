import csv
import json
import sys

from compressbench.types import BenchmarkResult


def output_results(results: list[BenchmarkResult], output_format: str = "text"):
    if output_format == "text":
        for r in results:
            print(f"Algorithm: {r.algorithm}")
            print(f"Compression ratio: {r.compression_ratio:.2f}")
            print(f"Compression time: {r.compression_time:.2f}s")
            print(f"Decompression time: {r.decompression_time:.2f}s")
            print(f"Input file: {r.input_file}")
            print("-" * 40)

    elif output_format == "json":
        json_data = [r.__dict__ for r in results]
        print(json.dumps(json_data, indent=2))

    elif output_format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["algorithm", "compression_ratio", "compression_time", "decompression_time", "input_file"])
        for r in results:
            writer.writerow(
                [
                    r.algorithm,
                    f"{r.compression_ratio:.2f}",
                    f"{r.compression_time:.2f}",
                    f"{r.decompression_time:.2f}",
                    r.input_file,
                ]
            )

    else:
        raise ValueError(f"Unknown output format: {output_format}")
