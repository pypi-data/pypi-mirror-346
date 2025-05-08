
import unittest

from arxivextract.extraction import ArXivExtractor
from arxivextract.data import ArticleEntryWithKeywords, BasicArticleEntry
from arxivextract.keywords import make_keyword_extractor
from arxivextract.keywordutils.keybert import KeywordBertKeywordExtractor
from arxivextract.keywordutils.yake import YakeKeywordExtractor


class TestKeywordExtraction(unittest.TestCase):
    def setUp(self):
        self.arxiv_extractor = ArXivExtractor(nb_articles_each_turn=2)

    def test_keybert_1(self):
        keyword_extractor = make_keyword_extractor('2025-04-02-keyword')
        assert isinstance(keyword_extractor, KeywordBertKeywordExtractor)

        all_article_entries = self.arxiv_extractor._partial_retrieve_articles('20250327')
        assert isinstance(all_article_entries[0], BasicArticleEntry)
        all_article_entries = [
            ArticleEntryWithKeywords.make_entry_by_adding_keywords(entry, keyword_extractor)
            for entry in all_article_entries
        ]
        assert isinstance(all_article_entries[0], ArticleEntryWithKeywords)

    def test_keybert_2(self):
        keyword_extractor = make_keyword_extractor('2025-04-23-keyword')
        assert isinstance(keyword_extractor, KeywordBertKeywordExtractor)

        all_article_entries = self.arxiv_extractor._partial_retrieve_articles('20250327')
        assert isinstance(all_article_entries[0], BasicArticleEntry)
        all_article_entries = [
            ArticleEntryWithKeywords.make_entry_by_adding_keywords(entry, keyword_extractor)
            for entry in all_article_entries
        ]
        assert isinstance(all_article_entries[0], ArticleEntryWithKeywords)

    def test_yake(self):
        keyword_extractor = make_keyword_extractor('2025-05-07-keyword')
        assert isinstance(keyword_extractor, YakeKeywordExtractor)

        all_article_entries = self.arxiv_extractor._partial_retrieve_articles('20250327')
        assert isinstance(all_article_entries[0], BasicArticleEntry)
        all_article_entries = [
            ArticleEntryWithKeywords.make_entry_by_adding_keywords(entry, keyword_extractor)
            for entry in all_article_entries
        ]
        assert isinstance(all_article_entries[0], ArticleEntryWithKeywords)



if __name__ == '__main__':
    unittest.main()
