# Tasks4 Experiment: OpenAI Chat Completions API

This is a standalone experiment fulfilling the AI Agent requirement. The script connects to the OpenAI API to summarize multi-sentence task descriptions into short, action-oriented phrases.

## ⚠️ Setup Requirements

1.  **Dependencies:** Ensure the `openai` library is installed (handled by `uv add openai`).
2.  **API Key:** This script requires a valid OpenAI API key to be set in your environment.

## 🔑 How to Run

1.  **Navigate:** Change directory into `tasks4`.
2.  **Set Environment Variable:** Run the following command, replacing the placeholder with your actual key. This MUST be done in the same terminal session as the run command.

    ```bash
    $env:OPENAI_API_KEY="sk-YOUR_KEY_HERE"
    ```

3.  **Execute Program:** Run the application to see the summarized output for the two sample tasks:

    ```bash
    python -m uv run tasks4
    ```