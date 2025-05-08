"""Calculate embedding features."""

# pylint: disable=global-statement
import pandas as pd
import tqdm
from sentence_transformers import SentenceTransformer

from .columns import DELIMITER, EMBEDDING_COLUMN

_MODEL = None


def _provide_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-mpnet-base-v2")
    return _MODEL


def embedding_process(df: pd.DataFrame) -> pd.DataFrame:
    """Process the embeddings for any text columns."""
    model = _provide_model()
    for column in tqdm.tqdm(
        df.select_dtypes(include="object").columns.tolist(),
        desc="Text embedding processing",
    ):
        texts = df[column].unique().tolist()
        embeddings = model.encode(texts)
        for count, text in enumerate(texts):
            embedding = embeddings[count].tolist()
            for embedding_index, value in enumerate(embedding):
                embedding_col = DELIMITER.join(
                    [column, EMBEDDING_COLUMN, str(embedding_index)]
                )
                if embedding_col not in df.columns.values.tolist():
                    df[embedding_col] = None
                df[df[column] == text][embedding_col] = value
    return df
