from typing import Generator

from sklearn.feature_extraction.text import TfidfVectorizer

from matchescu.blocking import Blocker, Block
from matchescu.blocking._tokenization import tokenize_reference
from matchescu.reference_store.id_table._protocol import IdTable


class TfIdfBlocker(Blocker):
    def __init__(self, id_table: IdTable, min_score: float = 0.1):
        super().__init__(id_table)
        self._min_score = min_score

    def __call__(self) -> Generator[Block, None, None]:
        refs = list(self._id_table)
        corpus = [" ".join(tokenize_reference(ref)) for ref in refs]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        token_inverted_map = vectorizer.get_feature_names_out()
        blocks: dict[str, Block] = {}
        for idx, ref in enumerate(refs):
            tfidf_scores = tfidf_matrix[idx].toarray().flatten()
            for score_idx, score in enumerate(tfidf_scores):
                if score < self._min_score:
                    continue
                score_token = token_inverted_map[score_idx]
                block = blocks.get(score_token, Block(score_token))
                block.append(ref.id)
                blocks[score_token] = block
        yield from blocks.values()
