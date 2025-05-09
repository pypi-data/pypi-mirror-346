# logycon-pipeline

A simple pipeline runner for Python tasks that allows you to define and execute a series of tasks in sequence.

## Installation

```bash
pip install logycon-pipeline
```

## Usage

1. Create a pipeline specification file (e.g., `pipeline.json`):

```json
{
  "name": "my-pipeline",
  "version": "1.0.0",
  "description": "My awesome pipeline",
  "tasks": [
    {
      "name": "task1",
      "script": "./scripts/task1.py",
      "env": {
        "CUSTOM_VAR": "value"
      }
    },
    {
      "name": "task2",
      "script": "./scripts/task2.py"
    }
  ]
}
```

2. Use the pipeline in your code:

```python
from logycon_pipeline import Pipeline

async def main():
    pipeline = Pipeline('./pipeline.json')
    try:
        results = await pipeline.run()
        print('Pipeline completed successfully:', results)
    except Exception as error:
        print('Pipeline failed:', error)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

## Task Scripts

Each task script should be a Python script that:
1. Performs the required operations
2. Outputs its result as a JSON string on the last line of stdout
3. Returns 0 on success, non-zero on failure

Example task script:

```python
# scripts/task1.py
import json
import sys

def main():
    # Do something
    result = {"status": "success", "data": "some data"}
    print(json.dumps(result))
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

## API

### Pipeline

The main class for running pipelines.

#### Constructor

```python
def __init__(self, spec_path: str)
```

Creates a new pipeline instance from a specification file.

#### Methods

```python
async def run() -> List[TaskResult]
```

Runs all tasks in the pipeline and returns a list of results.

### Types

```python
class Task:
    name: str
    script: str
    env: Optional[Dict[str, str]]

class PipelineSpec:
    name: str
    version: str
    description: str
    tasks: List[Task]

class TaskResult:
    task: str
    success: bool
    data: Optional[Any]
    error: Optional[str]
```

## License

MIT 