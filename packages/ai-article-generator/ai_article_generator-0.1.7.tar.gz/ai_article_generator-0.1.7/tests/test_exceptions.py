import pytest
from article_generator.exceptions import ArticleGenerationError


def test_article_generation_error():
    with pytest.raises(ArticleGenerationError):
        raise ArticleGenerationError("Test error")
