import pytest
from article_generator.generator import ArticleGenerator


class DummyAIClient:
    def __init__(self, *args, **kwargs):
        pass

    def generate(self, prompt, system_prompt=None, **kwargs):
        # Return a dummy JSON string for testing
        return '{"title": "Test Title", "subtitle": "Test Subtitle"}'


# Patch ArticleGenerator to use DummyAIClient for tests
def patch_ai_client(monkeypatch):
    from article_generator import generator

    monkeypatch.setattr(generator, "AIClient", DummyAIClient)


def test_article_generator_success(monkeypatch):
    patch_ai_client(monkeypatch)
    instructions = {
        "Article Header": {
            "instructions": "Write a header.",
            "response_format": {"title": "Title", "subtitle": "Subtitle"},
            "html_template": "<h1>{title}: {subtitle}</h1>",
        }
    }
    additional_data = {"keywords": ["AI", "journalism"]}
    generator = ArticleGenerator(
        instructions=instructions,
        additional_data=additional_data,
        article_type="feature",
    )
    html_sections = generator.generate()
    assert "Article Header" in html_sections
    assert "Test Title" in html_sections["Article Header"]
    assert "Test Subtitle" in html_sections["Article Header"]


def test_article_generator_invalid_type():
    instructions = {}
    additional_data = {}
    with pytest.raises(ValueError):
        ArticleGenerator(
            instructions=instructions,
            additional_data=additional_data,
            article_type="invalid_type",
        )


def test_article_generator_with_all_optional_args(monkeypatch):
    patch_ai_client(monkeypatch)
    instructions = {
        "Article Header": {
            "instructions": "Write a header.",
            "response_format": {"title": "Title", "subtitle": "Subtitle"},
            "html_template": "<h1>{title}: {subtitle}</h1>",
        }
    }
    additional_data = {"keywords": ["AI", "journalism"]}
    generator = ArticleGenerator(
        instructions=instructions,
        additional_data=additional_data,
        article_type="feature",
        system_prompt="Custom system prompt.",
        model="gpt-4o-mini",
    )
    html_sections = generator.generate()
    assert "Article Header" in html_sections
    assert "Test Title" in html_sections["Article Header"]
    assert "Test Subtitle" in html_sections["Article Header"]


def test_article_generator_with_only_required_args(monkeypatch):
    patch_ai_client(monkeypatch)
    instructions = {
        "Article Header": {
            "instructions": "Write a header.",
            "response_format": {"title": "Title", "subtitle": "Subtitle"},
            "html_template": "<h1>{title}: {subtitle}</h1>",
        }
    }
    additional_data = {"keywords": ["AI", "journalism"]}
    generator = ArticleGenerator(
        instructions=instructions, additional_data=additional_data
    )
    html_sections = generator.generate()
    assert "Article Header" in html_sections
    assert "Test Title" in html_sections["Article Header"]
    assert "Test Subtitle" in html_sections["Article Header"]
