from openai import OpenAI
import os
import re
from dotenv import load_dotenv

def extract_python_code(response_text: str) -> str:
    """
    Extracts the Python code block from the LLM's response.
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
You are an expert LangChain developer. Your task is to write a complete Python script for a LangChain workflow.

**Hard Rules:**
1.  **File Location:** The user will save your code in a file at `my_project/src/main.py`.
2.  **.env Configuration:** The script MUST get ALL of its configuration from a `.env` file located at the project root (`my_project/.env`).
3.  **dotenv Requirement:** To load the `.env` file from the parent directory, the script must use `load_dotenv(find_dotenv())` from the `python-dotenv` library.
4.  **Client Initialization:** The `ChatOpenAI` client MUST be initialized using all the loaded environment variables. Handle type casting and provide sensible defaults.
5.  **Clarity and Runnable:** The code must be clean, well-commented, and ready to run.

**Correct Code Structure Example:**
```python
import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load the .env file from the project root
load_dotenv(find_dotenv())

def main():
    \"\"\"The main execution function.\"\"\"
    # --- 1. Load ALL configuration from environment variables ---
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    model_name = os.getenv("PRIMARY_MODEL", "gpt-4")
    temperature = float(os.getenv("TEMPERATURE", 0.7))
    top_p = float(os.getenv("TOP_P", 0.9))
    max_tokens = int(os.getenv("MAX_TOKENS", 2000))

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    # --- 2. Initialize the LLM client with loaded settings ---
    llm = ChatOpenAI(
        base_url=base_url,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        api_key=api_key
    )

    # --- 3. LangChain implementation based on the user's prompt goes here ---
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
