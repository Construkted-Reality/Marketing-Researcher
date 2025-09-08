import json
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
        "--max-points",
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


def test_json_dump_creation(tmp_path: Path):
    """
    Test that JSON dump is created and contains canonical step-2 input.
    Uses dummy mode to avoid LLM calls.
    """
    # Set dummy test mode
    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "test_json_dump_creation"
    
    json_output = tmp_path / "pain_points.json"
    md_output = tmp_path / "test_output.md"
    
    cmd = [
        sys.executable,
        "spt_researcher.py",
        "--topic",
        "test topic",
        "--output",
        str(md_output),
        "--pain-points-output",
        str(json_output),
        "--max-points",
        "3",
        "--verbose",
    ]

    result = subprocess.run(
        cmd,
        cwd=os.getcwd(),
        capture_output=True,
        text=True,
        timeout=30,  # Fast execution in dummy mode
        env=env,
    )

    # Basic assertions
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert json_output.is_file(), "JSON dump file was not created."
    assert md_output.is_file(), "Output markdown file was not created."
    
    # Validate JSON structure
    with json_output.open("r") as f:
        pain_points_data = json.load(f)
    
    assert "topic" in pain_points_data
    assert "pain_points" in pain_points_data
    assert "meta" in pain_points_data
    assert pain_points_data["topic"] == "test topic"
    assert isinstance(pain_points_data["pain_points"], list)
    assert len(pain_points_data["pain_points"]) == 3  # max-points set to 3
    assert pain_points_data["meta"]["parser"] == "dummy"
    
    # Validate that pain points match expected dummy pattern
    for i, point in enumerate(pain_points_data["pain_points"], 1):
        assert point == f"Dummy pain point {i}"
    
    print(f"\n--- JSON dump validated: {json_output} ---")
    print(json.dumps(pain_points_data, indent=2))


def test_pain_points_input_override(tmp_path: Path):
    """
    Test --pain-points-input flag loads existing JSON and skips step-1.
    """
    # Create a mock JSON file
    mock_json = tmp_path / "mock_pain_points.json"
    mock_data = {
        "topic": "override test",
        "pain_points": [
            "Mock pain point 1",
            "Mock pain point 2"
        ],
        "meta": {
            "count": 2,
            "generated_at": "2024-01-01T00:00:00Z",
            "source": "test_mock",
            "max_points": 10,
            "parser": "mock"
        }
    }
    
    with mock_json.open("w") as f:
        json.dump(mock_data, f, indent=2)
    
    # Set dummy test mode (should be bypassed due to input override)
    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "test_pain_points_input_override"
    
    json_output = tmp_path / "canonical_dump.json"
    md_output = tmp_path / "test_output.md"
    
    cmd = [
        sys.executable,
        "spt_researcher.py",
        "--topic",
        "ignored topic",  # Should be overridden by JSON
        "--output",
        str(md_output),
        "--pain-points-input",
        str(mock_json),
        "--pain-points-output",
        str(json_output),
        "--verbose",
    ]

    result = subprocess.run(
        cmd,
        cwd=os.getcwd(),
        capture_output=True,
        text=True,
        timeout=30,  # Fast execution since no generation
        env=env,
    )

    # Basic assertions
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert json_output.is_file(), "Canonical JSON dump was not created."
    assert md_output.is_file(), "Output markdown file was not created."
    
    # Validate that JSON was loaded correctly
    with json_output.open("r") as f:
        canonical_data = json.load(f)
    
    assert canonical_data["topic"] == "override test"
    assert canonical_data["pain_points"] == ["Mock pain point 1", "Mock pain point 2"]
    assert canonical_data["meta"]["parser"] == "mock"
    
    # Check that stdout indicates step-1 was skipped
    assert "Loaded 2 pain points from" in result.stdout
    assert "Skipping step-1 generation" in result.stdout
    
    print(f"\n--- Input override test passed ---")
    print("Step-1 generation was successfully bypassed")


def test_human_readable_markdown(tmp_path: Path):
    """
    Test --pain-points-markdown flag creates human-readable output.
    Uses dummy mode to avoid LLM calls.
    """
    # Set dummy test mode
    env = os.environ.copy()
    env["PYTEST_CURRENT_TEST"] = "test_human_readable_markdown"
    
    json_output = tmp_path / "pain_points.json"
    md_output = tmp_path / "test_output.md"
    hr_md_output = tmp_path / "human_readable.md"
    
    cmd = [
        sys.executable,
        "spt_researcher.py",
        "--topic",
        "markdown test topic",
        "--output",
        str(md_output),
        "--pain-points-output",
        str(json_output),
        "--pain-points-markdown",
        str(hr_md_output),
        "--max-points",
        "3",
        "--verbose",
    ]

    result = subprocess.run(
        cmd,
        cwd=os.getcwd(),
        capture_output=True,
        text=True,
        timeout=30,  # Fast execution in dummy mode
        env=env,
    )

    # Basic assertions
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert json_output.is_file(), "JSON dump file was not created."
    assert hr_md_output.is_file(), "Human-readable markdown file was not created."
    
    # Validate markdown content
    with hr_md_output.open("r") as f:
        md_content = f.read()
    
    assert "# Pain Points for Topic: markdown test topic" in md_content
    assert "This is a human-readable version" in md_content
    assert "1. Dummy pain point 1" in md_content
    assert "2. Dummy pain point 2" in md_content
    assert "3. Dummy pain point 3" in md_content
    assert "Parser: dummy" in md_content
    
    print(f"\n--- Human-readable markdown validated: {hr_md_output} ---")
    print(md_content[:200] + "...")


def test_json_parsing_functions():
    """
    Unit test for parse_pain_points function with different input formats.
    """
    # Import the function
    import sys
    sys.path.insert(0, '.')
    from spt_researcher import parse_pain_points
    
    # Test JSON parsing
    json_input = '''
    {
        "topic": "test",
        "pain_points": [
            {"id": "PP01", "idea": "Test pain point 1", "description": "Test description"},
            {"id": "PP02", "idea": "Test pain point 2", "description": "Test description"}
        ],
        "meta": {"generator": "test"}
    }
    '''
    
    result = parse_pain_points(json_input, "test", 10, verbose=True)
    assert result["topic"] == "test"
    assert len(result["pain_points"]) == 2
    assert result["pain_points"][0] == "Test pain point 1"
    assert result["meta"]["parser"] == "json"
    
    # Test fallback parsing with noise
    fallback_input = '''
    Source: https://example.com
    Title: Some title
    - Real pain point 1
    Try again
    • Real pain point 2
    Please enable Javascript
    * Real pain point 3
    '''
    
    result = parse_pain_points(fallback_input, "test", 10, verbose=True)
    assert result["topic"] == "test"
    assert len(result["pain_points"]) == 3
    assert "Real pain point 1" in result["pain_points"]
    assert result["meta"]["parser"] == "fallback"
    
    # Ensure noise was filtered out
    pain_points_text = " ".join(result["pain_points"])
    assert "Source:" not in pain_points_text
    assert "Try again" not in pain_points_text
    assert "Please enable Javascript" not in pain_points_text
    
    print("\n--- JSON parsing functions validated ---")
    print(f"JSON parser: {result['pain_points']}")