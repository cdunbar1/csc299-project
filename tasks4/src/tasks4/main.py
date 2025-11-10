# tasks4/src/tasks4/main.py
import os
import sys
from openai import OpenAI
from typing import List, Dict

PARAGRAPH_TASKS: List[Dict[str, str]] = [
    {
        "id": "T1",
        "description": (
            "The first item requires me to conduct a thorough analysis of the market "
            "trends across all Q4 reports from major competitors. This involves downloading "
            "the data, creating pivot tables to identify growth segments, and synthesizing "
            "a three-page summary report by the end of the business day Tuesday."
        )
    },
    {
        "id": "T2",
        "description": (
            "We need to urgently fix the long-standing bug where user profile photos "
            "fail to load after a password reset. This bug is currently impacting 5% "
            "of our daily active users. The fix requires updating the authentication "
            "middleware and pushing a patch to the staging environment before Monday's review."
        )
    }
]

# ----------------------------------------------------
# MAIN LOGIC AND API CALL
# ----------------------------------------------------

def summarize_tasks_with_openai(tasks: List[Dict[str, str]]):
    """
    Connects to the OpenAI API (GPT-3.5 or similar) and summarizes 
    each paragraph-length task description into a short phrase.
    """
    print("--- Starting AI Summarization Experiment (tasks4) ---")
    
    # Check for API Key in environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("\nERROR: OPENAI_API_KEY environment variable is not set.")
        print("Please set your API key before running the script.")
        # Exit gracefully if the key is missing
        sys.exit(1)

    try:
        # Initialize the OpenAI Client
        client = OpenAI()
        
        # Add a loop to summarize multiple tasks (Required by assignment)
        for task in tasks:
            task_description = task["description"]
            
            # This is the prompt that instructs the AI on the task
            system_prompt = (
                "You are a professional project manager. Your task is to condense the "
                "following detailed task description into a single, short, action-oriented "
                "phrase (5 words maximum)."
            )
            
            print(f"\nProcessing Task {task['id']}...")

            # --- API CALL ---
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using gpt-3.5-turbo for cost/speed
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task_description}
                ],
                max_tokens=15, # Keep the response short as requested
                temperature=0.1
            )
            # --- END API CALL ---
            
            # Extract and print the summarized result
            summary = response.choices[0].message.content.strip()
            print(f"  Input: {task_description[:60]}...")
            print(f"  Summary: **{summary}**")

    except Exception as e:
        print(f"\nAn error occurred during the API call: {e}")
        # Hint for common issues
        if "AuthenticationError" in str(e):
             print("Check your API key validity.")
        elif "RateLimitError" in str(e):
             print("You might have hit a usage limit.")
        sys.exit(1)

def main():
    """Main entry point for the tasks4 application."""
    summarize_tasks_with_openai(PARAGRAPH_TASKS)

if __name__ == "__main__":
    main()