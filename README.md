# Langchainer (LangChain AutoPlanner Generator)

This project is a tool that automatically generates complete, runnable LangChain projects based on a user's natural language requirements.

<details>
<summary>阅读简体中文说明 (Read in Simplified Chinese)</summary>

---

## Langchainer (LangChain 自动规划生成器)

本项目是一个工具，可以根据用户的自然语言需求，自动生成完整、可运行的 LangChain 项目。

### 如何运行生成器

1.  **安装依赖：**
    ```bash
    pip install -r requirements.txt
    ```

2.  **设置环境变量：**
    此生成器需要 API 凭据才能运行。
    *   将 `.env.example` 文件复制一份并重命名为 `.env`。
    *   打开 `.env` 文件，并将占位符值替换为您的实际凭据。

3.  **运行生成器：**
    从命令行执行生成器脚本，并提供一个提示：
    ```bash
    python3 src/generator.py --prompt "your desired workflow here"
    ```
    例如：
    ```bash
    python3 src/generator.py --prompt "一个将'hello world'从英语翻译成法语的简单链"
    ```

生成的项目将放置在 `./dist` 目录中。`./dist` 目录已通过 `.gitignore` 从版本控制中排除。

---
</details>

## How to Run the Generator

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Environment Variables:**
    This generator requires API credentials to function.
    *   Copy the `.env.example` file to a new file named `.env`.
    *   Open the `.env` file and fill in your actual credentials, replacing the placeholder values.

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
