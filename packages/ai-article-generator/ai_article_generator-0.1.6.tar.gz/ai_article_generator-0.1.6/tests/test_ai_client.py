import os
import pytest
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


def patch_openai(monkeypatch):
    import article_generator.ai_client as ai_client_mod

    dummy_openai = type(
        "DummyOpenAI", (), {"OpenAI": lambda *a, **k: DummyOpenAIClient()}
    )
    monkeypatch.setattr(ai_client_mod, "openai", dummy_openai)


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
