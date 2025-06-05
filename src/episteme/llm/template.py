PROMPT_TEMPLATE = """
Given the task: "{task}"

List the minimal prerequisite concepts someone would need to understand in order to perform this task effectively.

Return format:
{"concepts": ["concept1", "concept2", ...]}
""".strip()


def build_prompt(task: str) -> str:
    """
    Constructs a prompt string by injecting a task description into the template.

    Args:
        task (str): The user-defined task.

    Returns:
        str: A fully formatted prompt string.
    """
    return PROMPT_TEMPLATE.format(task=task)
