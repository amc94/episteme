## Episteme: `setup.py` Documentation

### Purpose

The `setup.py` script initializes the **Episteme** local SQLite database. It defines the foundational schema used to store:

* Learning tasks
* Prerequisite concepts
* Task-concept mappings
* Reflection logs tracking conceptual understanding

This script enables reproducible environment setup and serves as the first step in bootstrapping the Episteme system.

---

### Schema Summary

| Table              | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `tasks`            | Stores high-level learning goals or projects                     |
| `concepts`         | Stores individual knowledge units and their mastery status       |
| `task_concept_map` | Links tasks to their required concepts with optional annotations |
| `progress_logs`    | Timestamped user reflections tied to specific concepts           |

---

### Usage

Run the script from the command line:

```bash
python setup.py
```

This will:

* Create `episteme.db` in the local directory if it does not already exist
* Create all required tables using safe `CREATE TABLE IF NOT EXISTS` guards
* Print confirmation upon success

---

### Notes

* **Idempotent**: safe to run multiple times; does not overwrite data
* **Local-first**: no external services required
* **Default behavior**: all `created_at` fields are auto-timestamped

---

### Future Improvements (Planned)

* Schema version tracking
* Automatic backup of preexisting DB
* CLI integration to trigger schema setup from main interface
