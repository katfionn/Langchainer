from openai import OpenAI
import os
import re
from dotenv import load_dotenv

def extract_python_code(response_text: str) -> str:
    """
    Extracts the Python code block from the LLM's response.
    Handles responses with or without markdown fences and extra text.
    """
    match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    lines = response_text.split('\\n')
    start_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import'):
            start_index = i
            break
    if start_index != -1:
        return '\\n'.join(lines[start_index:]).strip()
    return response_text.strip()

def generate_langchain_code(prompt: str) -> str:
    """
    Uses an LLM to generate a single-file LangChain script based on a user's prompt.
    """
    load_dotenv()
    api_base_url = os.getenv("API_BASE_URL")
    api_key = os.getenv("API_KEY")

    if not api_base_url or not api_key:
        return "# ERROR: API_BASE_URL and API_KEY must be set in a .env file for the generator to work."

    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key
    )

    model_to_use = "google/gemma-3-27b-it"
    print(f"Using model: {model_to_use}")

    system_prompt = """
You are an expert LangChain developer. Your task is to write a complete, single-file, runnable Python script for a LangChain workflow based on the user's request.

**Hard Rules:**
1.  **Single File:** All code MUST be in a single Python script.
2.  **dotenv Requirement:** The script MUST use `python-dotenv` to load the `OPENAI_API_KEY` from a `.env` file.
3.  **JSON Configuration:** The script MUST load all other parameters (`base_url`, `primary_model`, `temperature`, `top_p`, `max_tokens`) from `ai_models.config.json`.
4.  **Client Initialization:** The `ChatOpenAI` client MUST be initialized using all the loaded parameters from both the `.env` and `.json` files.
5.  **Clarity and Runnable:** The code must be clean, well-commented, and ready to run.

**Correct Code Structure Example:**
```python
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

def load_config(config_file="ai_models.config.json"):
    \"\"\"Loads the model configuration from a JSON file.\"\"\"
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    \"\"\"The main execution function.\"\"\"
    # Load the API key from the environment
    my_api_key = os.getenv("OPENAI_API_KEY")
    if not my_api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    # Load model and endpoint configuration
    config = load_config()

    # Initialize the LLM using all settings from the config file and the .env file
    llm = ChatOpenAI(
        base_url=config.get("base_url"),
        model_name=config.get("primary_model"),
        temperature=config.get("temperature", 0.7),
        top_p=config.get("top_p", 0.9),
        max_tokens=config.get("max_tokens", 2000),
        api_key=my_api_key
    )

    # --- LangChain implementation based on the user's prompt goes here ---
    prompt_template = ChatPromptTemplate.from_template("Translate 'hello world' to French.")
    chain = prompt_template | llm
    result = chain.invoke({})
    print(result.content)

if __name__ == "__main__":
    main()
```
"""

    try:
        completion = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is my request: {prompt}"}
            ]
        )

        raw_response = completion.choices[0].message.content
        extracted_code = extract_python_code(raw_response)
        return extracted_code
    except Exception as e:
        return f"# An error occurred during code generation: {e}"
