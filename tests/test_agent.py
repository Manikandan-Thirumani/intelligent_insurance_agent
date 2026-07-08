from intelligent_insurance_agent.agent import classify_intent, generate_response
from intelligent_insurance_agent.Model.chat import ChatMessage, ChatModel


class StubLLMClient:
    def generate(self, prompt: str) -> str:
        return "Llama response about quotes"


def test_classify_claim_intent():
    assert classify_intent("I need help filing a claim after an accident") == "claim"


def test_generate_response_for_quote():
    response = generate_response("How much would a policy cost?")
    assert "quote" in response.lower()


def test_generate_response_uses_llm_client_when_available():
    response = generate_response("How much would a policy cost?", llm_client=StubLLMClient())
    assert "Llama response" in response


def test_chat_model_uses_injected_llm_client_for_context_queries():
    class ContextLLMClient:
        def generate(self, prompt: str) -> str:
            return "The annual premium is $1,260.00."

    chat_model = ChatModel(llm_client=ContextLLMClient())
    response = chat_model.generate([
        ChatMessage(role="user", content="What is the available premium?"),
        ChatMessage(role="assistant", content="Context:\nPremium Information\nAnnual Premium: $1,260.00\n\nQuestion: What is the available premium?"),
    ])

    assert "$1,260.00" in response
