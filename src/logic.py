from openai import OpenAI
import os
import re
from dotenv import load_dotenv

def extract_python_code(response_text: str) -> str:
    """
    Extracts the Python code block from the LLM's response.
    Handles responses with or without markdown fences and extra text.
    """
    # Regex to find a python code block, capturing the content inside
    match = re.search(r"```python\n(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no markdown fences are found, assume the whole response is code
    # but clean up potential conversational text.
    # A simple heuristic: find the first line that starts with 'import'
    lines = response_text.split('\\n')
    start_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import'):
            start_index = i
            break

    if start_index != -1:
        return '\\n'.join(lines[start_index:]).strip()

    # Fallback if no 'import' is found, return the original text stripped.
    return response_text.strip()

def generate_langchain_code(prompt: str) -> str:
    """
    Uses an LLM to generate a single-file LangChain script based on a user's prompt.
    """
    load_dotenv() # Load environment variables from .env file for the generator itself

    api_base_url = os.getenv("API_BASE_URL")
    api_key = os.getenv("API_KEY")

    if not api_base_url or not api_key:
        return "# ERROR: API_BASE_URL and API_KEY must be set in a .env file for the generator to work."

    client = OpenAI(
        base_url=api_base_url,
        api_key=api_key
    )

    # Correct the model name by removing the unsupported tag.
    model_to_use = "google/gemma-3-27b-it"
    print(f"Using model: {model_to_use}")

    system_prompt = """
You are an expert LangChain developer. Your task is to write a complete, single-file, runnable Python script for a LangChain workflow based on the user's request.

**Hard Rules:**
1.  **Single File:** All code MUST be in a single Python script.
2.  **dotenv Requirement:** The script MUST use the `python-dotenv` library. The first two lines of executable code must be `from dotenv import load_dotenv` and `load_dotenv()`.
3.  **API Key Handling:** The script MUST load the API key using `os.getenv()` AFTER calling `load_dotenv()`. The loaded API key must then be passed explicitly to the ChatOpenAI constructor like this: `llm = ChatOpenAI(..., api_key=your_loaded_api_key)`.
4.  **Configuration:** The script must load its model configuration from a JSON file named `ai_models.config.json`.
5.  **Clarity and Runnable:** The code must be clean, well-commented, and ready to run with a main execution block.

**Correct Code Structure Example:**
```python
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# The first two lines MUST be this to load the .env file.
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

    # Load model configuration
    config = load_config()

    # Initialize the LLM, passing the API key directly
    llm = ChatOpenAI(
        model_name=config.get("primary_model", "gpt-4"),
        temperature=config.get("temperature", 0.7),
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
