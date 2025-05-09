"""Tests for the pipeline package."""

import json
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from logycon_pipeline import Pipeline


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_task_script(temp_dir: Path) -> Path:
    """Create a sample task script that returns success."""
    script_path = temp_dir / "task.py"
    script_content = """
import json
import sys

def main():
    result = {"status": "success", "data": "test data"}
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""
    script_path.write_text(script_content)
    return script_path


@pytest.fixture
def pipeline_spec(temp_dir: Path, sample_task_script: Path) -> Path:
    """Create a sample pipeline specification file."""
    spec = {
        "name": "test-pipeline",
        "version": "1.0.0",
        "description": "Test pipeline",
        "tasks": [
            {
                "name": "test-task",
                "script": str(sample_task_script),
                "env": {"TEST_VAR": "test_value"},
            }
        ],
    }
    spec_path = temp_dir / "pipeline.json"
    spec_path.write_text(json.dumps(spec))
    return spec_path


@pytest.mark.asyncio
async def test_pipeline_initialization(pipeline_spec: Path) -> None:
    """Test pipeline initialization from spec file."""
    pipeline = Pipeline(str(pipeline_spec))
    assert pipeline.spec.name == "test-pipeline"
    assert pipeline.spec.version == "1.0.0"
    assert len(pipeline.spec.tasks) == 1
    assert pipeline.spec.tasks[0].name == "test-task"


@pytest.mark.asyncio
async def test_pipeline_run(pipeline_spec: Path) -> None:
    """Test pipeline execution."""
    pipeline = Pipeline(str(pipeline_spec))
    results = await pipeline.run()
    assert len(results) == 1
    result = results[0]
    assert result.task == "test-task"
    assert result.success is True
    assert result.data is not None
    data = result.data
    assert isinstance(data, dict)
    assert data["status"] == "success"
    assert data["data"] == "test data"


@pytest.mark.asyncio
async def test_pipeline_with_failing_task(temp_dir: Path) -> None:
    """Test pipeline with a failing task."""
    # Create a failing task script
    failing_script = temp_dir / "failing_task.py"
    failing_script.write_text(
        """
import sys
sys.exit(1)
"""
    )
    # Create pipeline spec with failing task
    spec = {
        "name": "test-pipeline",
        "version": "1.0.0",
        "description": "Test pipeline",
        "tasks": [{"name": "failing-task", "script": str(failing_script)}],
    }
    spec_path = temp_dir / "pipeline.json"
    spec_path.write_text(json.dumps(spec))
    # Run pipeline
    pipeline = Pipeline(str(spec_path))
    results = await pipeline.run()
    assert len(results) == 1
    result = results[0]
    assert result.task == "failing-task"
    assert result.success is False
    assert result.error is not None
