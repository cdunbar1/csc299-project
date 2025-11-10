# Tasks3 Iteration: Testing and Packaging

This directory contains the integration of the PKMS/Task software into a formal Python package (`tasks3`) and includes required unit tests using `pytest`.

## ⚙️ Setup and Verification

1.  **Dependencies:** Ensure `uv` is installed (`pip install uv`).
2.  **Navigate:** Change directory into `tasks3`.

## 🧪 Running Unit Tests (Required Deliverable)

The following command executes the 3 unit tests: the boilerplate test (`test_inc.py`) and the two logic tests (`test_pkms_logic.py`).

```bash
# Must be run from within the tasks3 directory
python -m uv run pytest