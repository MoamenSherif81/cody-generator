import json

from LLM.Scheme.AnswerQuestion import AnswerQuestion, AskQuestion


def AnswerPrompt(prom):
    # Convert to absolute path if it's not already
    import os

    dsl_rules_path = os.path.join(os.getcwd(),"Compiler_V3/Parser/dsl_grammar.lark")
    dsl_example_path=os.path.join(os.getcwd(),"LLM/Backend/dsl_examples/code1.dsl")
    print(dsl_rules_path)

    # Read the DSL rules
    with open(dsl_rules_path, 'r') as file:
        dsl_rules = file.read()
    with open(dsl_example_path, 'r') as file:
        dsl_example= file.read()
    PromptMessage = [
        {
            "role": "system",
            "content": (
                "You are an expert Frontend Developer that can generate webpage using our own custom DSL.\n"
                "Generate the dsl for the provided situation"
                f"Dsl Grammar with lark = {dsl_rules}\n"
                f"You have to Generate response JSON {json.dumps(AnswerQuestion.model_json_schema(), ensure_ascii=False)} according the Pydantic details.\n"
                "Use only valid dsl tokens and .\n"
                "Do not generate any introduction or conclusion."
                "Use a simple, visually appealing random color scheme, ensuring all selected colors belong to it."
                "you can send any css style to the dsl with argument value like 'text<font=(\"10px\")>' it will be translated to 'font : 10px' in css"
                f"example of valid dsl code {dsl_example}"
                "Use valid temp urls "
                "center elements as you can"
                "Be Creative"
            )
        },
        {
            "role": "user",
            "content": (
                "## Pydantic Details:\n"
                f"{json.dumps(AskQuestion.model_json_schema(), ensure_ascii=False)}\n\n"
                f"## Question :\n {prom} \n"
                "```json"
            )
        }
    ]
    prompt = ""
    for i in PromptMessage:
        prompt += str(i)
        prompt += "\n"
    return PromptMessage
