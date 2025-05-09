## Distributed Redis State Model

A lightweight Pydantic-based base class for keeping your model state in sync across multiple Python services via Redis.
Each instance is identified by a unique `id_` and will automatically read/write its fields to Redis whenever they change.

---

### Features

* **Pydantic model**: full data‐validation, parsing and type hints.
* **Automatic Redis sync**: reads from Redis on init and writes back on assignment.
* **Portable**: move instances between services (same class name + `id_`) and state stays in sync.
* **Minimal dependencies**: just `pydantic` and `redis-py`.

---

### Installation

```bash
pip install pydantic-state-manager
```

---

### Quickstart

```python
from src.base_redis_state_model import BaseRedisStateModel

class DistributedTaskState(BaseRedisStateModel):
    """
    Tracks the lifecycle state of a distributed task.
    """
    current_state: str = "scheduled"


# Create or load the state for “task_1”
task_state = DistributedTaskState(id_="task_1")

# Update the state; this writes immediately to Redis
task_state.current_state = "running"

# In another service/process (with same code):
# state = DistributedTaskState(id_="task_1")
# print(state.current_state)  # → "running"

task_state.current_state = "completed"
```

---

### How It Works

1. **Initialization**
   On `__init__`, the model attempts to fetch any existing JSON blob from Redis at key
   `"{ClassName}:{id_}"`. If found, it populates the model fields from that JSON; otherwise
   it uses the default values you defined in your subclass.

2. **Attribute Assignment**
   Whenever you set any field on your model, the base class overrides `__setattr__` to:

   * Validate the new value (via Pydantic)
   * Write it back to Redis under the same key

3. **Cross-Service Sync**
   As long as each service imports the same subclass name and gives it the same `id_`, any
   assignment in one process will be immediately visible to others when they next access the
   property (or reinstantiate the object).

---

### API Reference

#### `class BaseRedisStateModel(pydantic.BaseModel)`

| Parameter | Type  | Required | Description                                |
| --------- | ----- | -------- | ------------------------------------------ |
| `id_`     | `str` | Yes      | Unique identifier for this model instance. |


### Configuration

Under the hood, the Redis connection is managed via environment variables (or defaults):

* `STATE_MANAGER_REDIS_URL` (default: `redis://localhost:6379/0`)

You can override these at import time:

```python
import os
os.environ["STATE_MANAGER_REDIS_URL"] = "redis-prod.mycompany.internal"
```

---

### License

MIT © 2025 Ruslan Schalkenbajew
