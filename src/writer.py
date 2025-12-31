import os

def write_project_files(main_flow_code: str, requirements: str, readme: str, env_example: str, output_dir: str = "dist"):
    """
    Creates the output directory and writes all the generated project files
    with the new, consistent structure.
    """
    # Create the root and src directories
    dist_src_dir = os.path.join(output_dir, "src")
    os.makedirs(dist_src_dir, exist_ok=True)

    # Define file paths
    main_flow_path = os.path.join(dist_src_dir, "main.py")
    requirements_path = os.path.join(output_dir, "requirements.txt")
    readme_path = os.path.join(output_dir, "README.md")
    env_example_path = os.path.join(output_dir, ".env.example")

    # Write the main LangChain flow file to the new src directory
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

    # Write the .env.example file
    try:
        with open(env_example_path, "w") as f:
            f.write(env_example)
    except IOError as e:
        print(f"Error writing .env.example file: {e}")
        return

    print(f"Project successfully generated with the new structure in ./{output_dir}")
