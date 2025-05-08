
from abc import ABC, abstractmethod


class AbstractKeywordExtractor(ABC):
    @abstractmethod
    def extract_keywords(self, text: str) -> list[str]:
        pass


keyword_configs = {
    '2025-04-02-keyword': {
        'model': 'KeyBERT',
        'embed_model': 'all-MiniLM-L6-v2',
        'configs': {
            'keyphrase_ngram_range': (1, 3),
            'stop_words': 'english',
            'top_n': 5
        }
    },
    '2025-04-23-keyword': {
        'model': 'KeyBERT',
        'embed_model': 'allenai-specter',
        'configs': {
            'keyphrase_ngram_range': (1, 2),
            'stop_words': 'english',
            'top_n': 5
        }
    },
    '2025-05-07-keyword': {
        'model': 'YAKE'
    }
}
DEFAULT_SENTENCEEMBED = 'all-MiniLM-L6-v2'


def make_keyword_extractor(version: str) -> AbstractKeywordExtractor:
    if version not in keyword_configs.keys():
        raise ValueError(f'Keyword version {version} is not found.')

    keyword_extraction_model = keyword_configs[version].get('model')
    if keyword_extraction_model is None:
        raise ValueError('NoneType error!')
    if keyword_extraction_model == 'KeyBERT':
        from .keywordutils.keybert import KeywordBertKeywordExtractor

        return KeywordBertKeywordExtractor(
            keyword_configs[version].get('configs'),
            embed_model=keyword_configs[version].get('embed_model', DEFAULT_SENTENCEEMBED)
        )
    elif keyword_extraction_model == 'YAKE':
        from .keywordutils.yake import YakeKeywordExtractor

        return YakeKeywordExtractor()
    else:
        raise ValueError(f'Unknown keyword extraction model: {keyword_extraction_model}')
