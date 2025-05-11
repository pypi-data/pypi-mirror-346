import pytest
from article_generator.section import Section, SectionFactory


class DummyAIClient:
    def generate(self, prompt, system_prompt=None, **kwargs):
        return '{"title": "Test Title", "subtitle": "Test Subtitle"}'

    def generate_image(self, image_prompt, image_model, size, quality, n):
        if image_prompt == "error_image_prompt":
            raise ValueError("Simulated image generation error")
        return f"http://example.com/images/{image_prompt.replace(' ', '_')}.png"


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


# --- Tests for Image Generation in Sections ---


def test_section_generate_content_image_success():
    image_prompt_text = "A cute puppy playing"
    info = {
        "content_type": "image",
        "instructions": image_prompt_text,
        "response_format": {
            "image_url": "URL of the image"
        },  # For clarity, not strictly used by logic for images
        "html_template": "<img src='{image_url}' alt='Generated image' />",
        "image_model": "dall-e-test",
        "image_size": "256x256",
        "image_quality": "low",
    }
    section = Section(name="Puppy Image", info=info, ai_client=DummyAIClient(), data={})
    html_output = section.generate_content()
    expected_url = (
        f"http://example.com/images/{image_prompt_text.replace(' ', '_')}.png"
    )
    assert html_output == f"<img src='{expected_url}' alt='Generated image' />"


def test_section_generate_content_image_missing_instructions():
    info = {
        "content_type": "image",
        # "instructions": "Missing prompt", # Intentionally missing
        "html_template": "<img src='{image_url}' />",
    }
    section = Section("Test Image", info, DummyAIClient(), {})
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "Image generation section requires 'instructions'" in str(excinfo.value)


def test_section_generate_content_image_missing_template():
    info = {
        "content_type": "image",
        "instructions": "A test image",
        # "html_template": "<img src='{image_url}' />", # Intentionally missing
    }
    section = Section("Test Image", info, DummyAIClient(), {})
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "requires an 'html_template'" in str(excinfo.value)


def test_section_generate_content_image_template_no_image_url():
    info = {
        "content_type": "image",
        "instructions": "A test image",
        "html_template": "<p>This template is wrong</p>",  # Missing {image_url}
    }
    section = Section("Test Image", info, DummyAIClient(), {})
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "must contain '{image_url}'" in str(excinfo.value)


def test_section_generate_content_image_generation_fails():
    info = {
        "content_type": "image",
        "instructions": "error_image_prompt",  # Will cause DummyAIClient.generate_image to raise error
        "html_template": "<img src='{image_url}' />",
    }
    section = Section("Error Image", info, DummyAIClient(), {})
    with pytest.raises(ValueError) as excinfo:
        section.generate_content()
    assert "Failed to generate image for section" in str(excinfo.value)
    assert "Simulated image generation error" in str(excinfo.value)
