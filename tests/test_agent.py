from intelligent_insurance_agent.agent import classify_intent, generate_response


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
