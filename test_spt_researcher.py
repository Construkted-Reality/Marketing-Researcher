import os
import subprocess
import sys
from pathlib import Path

def test_spt_researcher_runs(tmp_path: Path):
    """
    Basic integration test:
    - Executes the script with a simple topic.
    - Checks that the output markdown file is created.
    - Does not assert on content (requires live LLM service).
    """
    # Ensure required environment variables are present for a minimal run
    required_vars = ["OPENAI_API_BASE", "OPENAI_MODEL_NAME"]
    for var in required_vars:
        if var not in os.environ:
            raise RuntimeError(f"Environment variable {var} must be set for the test.")

    output_file = tmp_path / "test_output.md"
    cmd = [
        sys.executable,
        "spt_researcher.py",
        "--topic",
        "sample topic for testing",
        "--output",
        str(output_file),
        "--max-insights",
        "5",
        "--verbose",
    ]

    result = subprocess.run(
        cmd,
        cwd=os.getcwd(),
        capture_output=True,
        text=True,
        timeout=180,  # allow up to 3 minutes for LLM processing
    )

    # Basic assertions
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert output_file.is_file(), "Output markdown file was not created."

    # Optional: print a snippet of the output for debugging
    print("\n--- Script stdout snippet ---")
    print("\n".join(result.stdout.splitlines()[:20]))