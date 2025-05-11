import pytest
from article_generator.section import Section, SectionFactory


class DummyAIClient:
    def generate(self, prompt, system_prompt=None, **kwargs):
        return '{"title": "Test Title", "subtitle": "Test Subtitle"}'


# Modify DummyAIClient for this test case to return appropriate JSON
class SeoDummyAIClient:
    def generate(self, prompt, system_prompt=None, **kwargs):
        return '{"seo_title": "Test SEO Title", "meta_description": "Test Meta Description"}'


class InvalidJsonAIClient:
    def generate(self, prompt, system_prompt=None, **kwargs):
        return "not a valid json string { nope ]"


class MissingFieldAIClient:
    def generate(self, prompt, system_prompt=None, **kwargs):
        # Simulates AI returning JSON that is valid but missing an expected field
        return '{"title": "Test Title Only"}'  # Missing 'subtitle'


def test_section_generate_content():
    info = {
        "instructions": "Write a header.",
        "response_format": {"title": "Title", "subtitle": "Subtitle"},
        "html_template": "<h1>{title}: {subtitle}</h1>",
    }
    section = Section(
        name="Article Header",
        info=info,
        ai_client=DummyAIClient(),
        data={"keywords": ["AI"]},
    )
    content = section.generate_content()
    assert content == "<h1>Test Title: Test Subtitle</h1>"


def test_section_generate_content_no_template():
    info = {
        "instructions": "Generate SEO data.",
        "response_format": {
            "seo_title": "SEO Title",
            "meta_description": "Meta Description",
        },
        # No html_template
    }

    section = Section(
        name="SEO Data",
        info=info,
        ai_client=SeoDummyAIClient(),
        data={"topic": "AI"},
    )
    content = section.generate_content()
    # If no html_template, content is a dictionary
    assert isinstance(content, dict)
    assert content["seo_title"] == "Test SEO Title"
    assert content["meta_description"] == "Test Meta Description"


def test_section_generate_content_invalid_json():
    info = {
        "instructions": "Test instructions.",
        "response_format": {"field": "Expected field"},
    }
    section = Section(
        name="Test Section",
        info=info,
        ai_client=InvalidJsonAIClient(),
        data={},
    )
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "AI response is not valid JSON" in str(excinfo.value)


def test_section_generate_content_missing_field_from_response_format():
    info = {
        "instructions": "Write a header.",
        "response_format": {
            "title": "Title",
            "subtitle": "Subtitle",
        },  # Expects title and subtitle
        # No html_template, so we are checking against response_format directly
    }
    section = Section(
        name="Article Header",
        info=info,
        ai_client=MissingFieldAIClient(),
        data={},
    )
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "Missing fields in AI response" in str(excinfo.value)
    assert "'subtitle'" in str(
        excinfo.value
    )  # Check that the missing key 'subtitle' is mentioned
    assert "expected from response_format" in str(excinfo.value)


def test_section_generate_content_missing_field_for_template():
    info = {
        "instructions": "Write a header.",
        "response_format": {
            "title": "Title"
        },  # Only require 'title' for response_format validation
        "html_template": "<h1>{title}: {subtitle}</h1>",  # Template requires subtitle
    }
    section = Section(
        name="Article Header with Template",
        info=info,
        ai_client=MissingFieldAIClient(),  # Returns only {"title": "Test Title Only"}
        data={},
    )
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "Missing fields in AI response" in str(excinfo.value)
    assert "'subtitle'" in str(
        excinfo.value
    )  # Check that the missing key 'subtitle' is mentioned
    assert "required by html_template" in str(excinfo.value)


def test_section_factory_create():
    factory = SectionFactory(DummyAIClient())
    info = {
        "instructions": "Write a header.",
        "response_format": {"title": "Title", "subtitle": "Subtitle"},
        "html_template": "<h1>{title}: {subtitle}</h1>",
    }
    section = factory.create("Article Header", info, {"keywords": ["AI"]})
    assert isinstance(section, Section)
    assert section.name == "Article Header"
