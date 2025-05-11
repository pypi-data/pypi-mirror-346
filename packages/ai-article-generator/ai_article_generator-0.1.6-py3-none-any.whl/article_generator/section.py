import json
import re


class Section:
    def __init__(self, name, info, ai_client, data):
        self.name = name
        self.info = info
        self.data = data
        self.ai_client = ai_client

    def generate_content(self):
        # Compose the prompt
        prompt = f"""
            You are generating structured content for the '{self.name}' section.

            Instructions:
            {self.info['instructions']}

            Your response must be a JSON object with these fields and formats:
            {json.dumps(self.info['response_format'], indent=2)}
        """

        html_template = self.info.get("html_template")

        if html_template:
            prompt += f"""

            The content will be inserted into this HTML template:
            {html_template}
            Ensure the generated JSON object contains all keys required by the template.
            """
        else:
            prompt += """

            You should return only the structured JSON object as specified.
            """

        if self.data:
            prompt += f"\nAdditional data to use:\n{json.dumps(self.data, indent=2)}"

        # Call the AI client
        response = self.ai_client.generate(
            prompt, response_format={"type": "json_object"}, temperature=0.3
        )

        # Parse the response as JSON
        try:
            content_json = json.loads(response)
        except Exception as e:
            raise ValueError(
                f"AI response is not valid JSON: {e}\nResponse: {response}"
            )

        # Validate that all keys from response_format are present in the AI's response
        expected_keys = set(self.info["response_format"].keys())
        actual_keys = set(content_json.keys())
        missing_keys_from_format = expected_keys - actual_keys
        if missing_keys_from_format:
            raise ValueError(
                f"Missing fields in AI response for {self.name} (expected from response_format): {list(missing_keys_from_format)}"
            )

        if html_template:
            template_fields = re.findall(r"\{(\w+)\}", html_template)
            missing_fields_for_template = [
                field for field in template_fields if field not in content_json
            ]
            if missing_fields_for_template:
                raise ValueError(
                    f"Missing fields in AI response for {self.name} (required by html_template): {missing_fields_for_template}"
                )
            # Fill the template with the AI's response
            return html_template.format(**content_json)
        else:
            # Return the raw JSON (Python dictionary) if no template is provided
            return content_json


class SectionFactory:
    def __init__(self, ai_client):
        self.ai_client = ai_client

    def create(self, name, info, data):
        # For now, always return Section, but can be extended for custom logic
        return Section(name, info, self.ai_client, data)
