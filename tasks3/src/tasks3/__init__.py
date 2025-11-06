# tasks3/src/tasks3/__init__.py
from .app import main as app_main 

def inc(n: int) -> int:
    return n + 1

# This is the entry point that uv run tasks3 calls
def main() -> None:
    # We call the main logic imported from app.py
    app_main() 

if __name__ == "__main__":
    main()