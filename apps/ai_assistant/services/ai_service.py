from integrations.ai.provider import AIProvider

class AIService:
    @classmethod
    def improve_description(cls, title: str, raw_description: str, category_name: str = '') -> str:
        return AIProvider.improve_description(title, raw_description, category_name)

    @classmethod
    def suggest_price(cls, title: str, category_name: str = '') -> dict:
        return AIProvider.suggest_price(title, category_name)

    @classmethod
    def search_assist(cls, query: str) -> dict:
        return AIProvider.search_assist(query)

    @classmethod
    def call_gemini(cls, prompt: str) -> str:
        return AIProvider.call_gemini(prompt)
