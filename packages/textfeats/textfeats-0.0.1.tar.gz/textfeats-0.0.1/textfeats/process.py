"""The main process function."""

import pandas as pd

from .embedding_process import embedding_process


def process(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Process the dataframe for text features."""
    df = embedding_process(df)
    return df[sorted(df.columns.values.tolist())]
