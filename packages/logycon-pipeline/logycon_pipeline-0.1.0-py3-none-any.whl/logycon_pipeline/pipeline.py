"""
Core pipeline implementation
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    """Represents a single task in the pipeline"""

    name: str
    script: str
    env: Optional[Dict[str, str]] = Field(default_factory=lambda: {})


class PipelineSpec(BaseModel):
    """Pipeline specification"""

    name: str
    version: str
    description: str
    tasks: List[Task]


class TaskResult(BaseModel):
    """Result of a task execution"""

    task: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class Pipeline:
    """Main pipeline runner class"""

    def __init__(self, spec_path: str) -> None:
        """
        Initialize pipeline from specification file

        Args:
            spec_path: Path to the pipeline specification JSON file
        """
        self.spec_path = Path(spec_path)
        with open(self.spec_path) as f:
            spec_data = json.load(f)
        self.spec = PipelineSpec(**spec_data)

    async def run(self) -> List[TaskResult]:
        """
        Run all tasks in the pipeline

        Returns:
            List of task results
        """
        results = []
        for task in self.spec.tasks:
            try:
                # Prepare environment
                env = dict(task.env) if task.env else {}
                # Run the task script using the current Python interpreter
                process = subprocess.run(
                    [sys.executable, task.script],
                    capture_output=True,
                    text=True,
                    env=env,
                )
                if process.returncode == 0:
                    # Parse the last line as JSON for the result
                    output_lines = process.stdout.strip().split("\n")
                    if output_lines:
                        try:
                            data = json.loads(output_lines[-1])
                        except json.JSONDecodeError:
                            data = None
                    else:
                        data = None
                    results.append(TaskResult(task=task.name, success=True, data=data))
                else:
                    results.append(TaskResult(task=task.name, success=False, error=process.stderr))
            except Exception as e:
                results.append(TaskResult(task=task.name, success=False, error=str(e)))
        return results
