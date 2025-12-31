import os

def write_project_files(main_flow_code: str, requirements: str, readme: str, output_dir: str = "dist"):
    """
    Creates the output directory and writes all the generated project files.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define file paths
    main_flow_path = os.path.join(output_dir, "main_langchain_flow.py")
    requirements_path = os.path.join(output_dir, "requirements.txt")
    readme_path = os.path.join(output_dir, "README.md")

    # Write the main LangChain flow file
    try:
        with open(main_flow_path, "w") as f:
            f.write(main_flow_code)
    except IOError as e:
        print(f"Error writing main flow file: {e}")
        return

    # Write the requirements file
    try:
        with open(requirements_path, "w") as f:
            f.write(requirements)
    except IOError as e:
        print(f"Error writing requirements file: {e}")
        return

    # Write the README file
    try:
        with open(readme_path, "w") as f:
            f.write(readme)
    except IOError as e:
        print(f"Error writing README file: {e}")
        return

    print(f"Project successfully generated in ./{output_dir}")
