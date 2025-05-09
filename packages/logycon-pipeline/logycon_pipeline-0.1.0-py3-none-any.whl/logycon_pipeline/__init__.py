"""
Logycon Pipeline - A simple pipeline runner for Python tasks
"""

from .pipeline import Pipeline, PipelineSpec, Task, TaskResult

__version__ = "0.1.0"
__all__ = ["Pipeline", "Task", "PipelineSpec", "TaskResult"]
