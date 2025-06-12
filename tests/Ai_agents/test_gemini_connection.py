from Ai_Agents import Gemini


def test_connect_gemini():
    response = Gemini().request("test")
    assert response is not None, "Gemini response is None"
