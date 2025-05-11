import os

import httpx
import openai
from dotenv import load_dotenv

load_dotenv()

# General stylistic guidelines to append to specific prompts
GENERAL_STYLE_GUIDELINES = (
    "Strive for clarity, conciseness, and a logical flow. "
    "Prioritize active voice. Vary sentence structures and beginnings for natural readability. "
    "Use vivid, precise language, and integrate keywords organically."
)

DEFAULT_SYSTEM_PROMPTS = {
    "review": (
        "You are an expert reviewer and SEO specialist generating structured, insightful, and engaging review content. "
        "Ensure the writing is optimized for search engines: use relevant keywords naturally, write clear meta descriptions, "
        f"and structure content for readability and user engagement. {GENERAL_STYLE_GUIDELINES}"
    ),
    "news": (
        "You are a professional journalist and SEO expert writing clear, concise, and factual news articles. "
        f"Optimize for search engines by using relevant keywords, concise headlines, and structured content. {GENERAL_STYLE_GUIDELINES}"
    ),
    "guide": (
        "You are an expert educator and SEO specialist writing step-by-step guides for beginners. "
        "Ensure the guide is optimized for search engines: use clear headings, relevant keywords, and actionable steps. "
        f"{GENERAL_STYLE_GUIDELINES}"
    ),
    "feature": (
        "You are a creative writer and SEO expert crafting in-depth feature articles. "
        "Write engaging, well-structured content that is optimized for search engines and user engagement. "
        f"{GENERAL_STYLE_GUIDELINES}"
    ),
    "generic": (
        "You are a helpful and knowledgeable content writer with strong SEO skills. "
        f"Write clear, engaging, and search-optimized content. {GENERAL_STYLE_GUIDELINES}"
    ),
}


class AIClient:
    def __init__(
        self,
        article_type: str = "generic",
        system_prompt: str = None,
        model: str = "gpt-4o-mini",
    ):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPTS.get(
            article_type, DEFAULT_SYSTEM_PROMPTS["generic"]
        )
        http_client = httpx.Client()
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"), http_client=http_client
        )
        self.model = model

    def generate_image(
        self,
        image_prompt: str,
        image_model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        n: int = 1,
    ) -> str:
        """Generates an image using DALL·E and returns the image URL."""
        try:
            response = self.client.images.generate(
                model=image_model,
                prompt=image_prompt,
                size=size,
                quality=quality,
                n=n,
                response_format="url",  # Request URL for simplicity
            )
            # Assuming n=1, so we take the first image URL
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                if image_url:
                    return image_url
                else:
                    raise ValueError("API response did not contain an image URL.")
            else:
                raise ValueError("API response did not contain image data.")
        except openai.APIError as e:
            # Handle specific OpenAI API errors or re-raise as a more generic error
            raise ValueError(f"OpenAI API error during image generation: {e}") from e
        except Exception as e:
            # Catch any other unexpected errors
            raise ValueError(f"Unexpected error during image generation: {e}") from e

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            **{k: v for k, v in kwargs.items()},
        )
        return response.choices[0].message.content
