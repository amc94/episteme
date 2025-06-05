# template.py

HEADERS = {
    "default": "Given a task, output its prerequisite concepts in JSON.",
    "concise": "Output prerequisite concepts for this task.",
    "elaborate": "You are a curriculum planner. Analyze the task and list all prerequisite concepts in JSON format.",
}

RETURN_FORMAT = 'Return format: { "concepts": [...] }'


def build_prompt(task: str, header_type: str = "default") -> str:
    if header_type not in HEADERS:
        raise ValueError(f"Unknown header_type: {header_type}")

    header = HEADERS[header_type]
    return f"{header}\nTask: {task}\n{RETURN_FORMAT}"
