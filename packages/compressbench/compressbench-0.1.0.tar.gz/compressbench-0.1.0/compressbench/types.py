from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    algorithm: str
    compression_ratio: float
    compression_time: float
    decompression_time: float
    input_file: str
