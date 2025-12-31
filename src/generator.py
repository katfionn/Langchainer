import argparse
import os
from logic import generate_langchain_code
from writer import write_project_files

def load_template(template_name: str) -> str:
    """Loads the content of a template file."""
    template_path = os.path.join("src", "templates", template_name)
    with open(template_path, "r") as f:
        return f.read()

def get_static_files_content():
    """
    Loads the content for the static files from the templates directory.
    """
    requirements_content = load_template("requirements.txt.template")
    readme_content = load_template("README.md.template")
    env_example_content = load_template("env.example.template")

    return requirements_content, readme_content, env_example_content

def main():
    """
    The main entry point for the LangChain AutoPlanner Generator.
    """
    parser = argparse.ArgumentParser(description="Generate a LangChain project based on a user prompt.")
    parser.add_argument("--prompt", type=str, required=True, help="The user's requirement for the LangChain workflow.")
    args = parser.parse_args()

    print(f"Generating LangChain project for prompt: '{args.prompt}'")

    # 1. Generate the core LangChain code
    main_flow_code = generate_langchain_code(args.prompt)

    # 2. Get the content for the static files from templates
    requirements, readme, env_example = get_static_files_content()

    # 3. Write all the files to the ./dist directory
    write_project_files(
        main_flow_code=main_flow_code,
        requirements=requirements,
        readme=readme,
        env_example=env_example
    )

if __name__ == "__main__":
    main()
