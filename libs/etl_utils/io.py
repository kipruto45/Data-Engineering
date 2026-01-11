import pandas as pd
from typing import Iterator


def incremental_csv_chunks(path: str, chunk_size: int = 100_000) -> Iterator[pd.DataFrame]:
    """Yield CSV chunks as DataFrames for memory-friendly processing."""
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        yield chunk
