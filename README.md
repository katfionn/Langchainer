# Langchainer (LangChain AutoPlanner Generator)

This project is a tool that automatically generates complete, runnable LangChain projects based on a user's natural language requirements.

## How to Run the Generator

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Environment Variables:**
    This generator requires API credentials to function.
    *   Create a file named `.env` in the root of this project.
    *   Add the following lines, replacing the placeholder values with your actual credentials:
        ```
        API_BASE_URL="your_api_base_url_here"
        API_KEY="your_api_key_here"
        ```

3.  **Run the Generator:**
    Execute the generator script from the command line, providing a prompt:
    ```bash
    python3 src/generator.py --prompt "your desired workflow here"
    ```
    For example:
    ```bash
    python3 src/generator.py --prompt "a simple chain that translates 'hello world' from English to French"
    ```

The generated project will be placed in the `./dist` directory. The `./dist` directory is excluded from version control via `.gitignore`.
