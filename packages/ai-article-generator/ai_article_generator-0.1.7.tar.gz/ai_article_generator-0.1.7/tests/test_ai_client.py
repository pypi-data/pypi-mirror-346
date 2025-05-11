import os
import pytest
import openai
from article_generator.ai_client import AIClient


class DummyOpenAIClient:
    class chat:
        class completions:
            @staticmethod
            def create(model, messages, **kwargs):
                class Response:
                    class Choice:
                        message = type("msg", (), {"content": "dummy response"})()

                    choices = [Choice()]

                return Response()

    class images:
        @staticmethod
        def generate(model, prompt, size, quality, n, response_format):
            if prompt == "error_prompt":
                # Raise a generic exception to test the AIClient's general error handling
                raise Exception("Simulated generic error from dummy image generation")
            if prompt == "no_url_prompt":

                class ImageDataNoUrl:
                    url = None

                class ResponseNoUrl:
                    data = [ImageDataNoUrl()]

                return ResponseNoUrl()
            if prompt == "no_data_prompt":

                class ResponseNoData:
                    data = []

                return ResponseNoData()

            class ImageData:
                url = "http://example.com/generated_image.png"

            class Response:
                data = [ImageData()]

            return Response()


def patch_openai(monkeypatch):
    import article_generator.ai_client as ai_client_mod

    dummy_openai_type = type(
        "DummyOpenAI", (), {"OpenAI": lambda *a, **k: DummyOpenAIClient()}
    )

    class PatchedOpenAIModule:
        OpenAI = lambda *a, **k: DummyOpenAIClient()
        APIError = openai.APIError

    monkeypatch.setattr(ai_client_mod, "openai", PatchedOpenAIModule)


def test_aiclient_init_with_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    assert client.api_key == "test-key"


def test_aiclient_init_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError):
        AIClient()


def test_aiclient_generate(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    result = client.generate("prompt")
    assert result == "dummy response"


def test_aiclient_generate_image_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    image_url = client.generate_image("A beautiful cat")
    assert image_url == "http://example.com/generated_image.png"


def test_aiclient_generate_image_api_error(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    with pytest.raises(ValueError) as excinfo:
        client.generate_image("error_prompt")
    assert "Unexpected error during image generation" in str(excinfo.value)
    assert "Simulated generic error from dummy image generation" in str(excinfo.value)


def test_aiclient_generate_image_no_url_in_response(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    with pytest.raises(ValueError) as excinfo:
        client.generate_image("no_url_prompt")
    assert "API response did not contain an image URL" in str(excinfo.value)


def test_aiclient_generate_image_no_data_in_response(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    patch_openai(monkeypatch)
    client = AIClient()
    with pytest.raises(ValueError) as excinfo:
        client.generate_image("no_data_prompt")
    assert "API response did not contain image data" in str(excinfo.value)
