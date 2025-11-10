# tasks4/src/tasks4/__init__.py

from .main import main as app_main

def inc(n: int) -> int:
    return n + 1

# This is the entry point that uv run tasks4 calls
def main() -> None:
    # Now we call the aliased function which runs the summarization logic
    app_main() 

if __name__ == "__main__":
    main()