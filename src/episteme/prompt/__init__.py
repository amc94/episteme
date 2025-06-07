from .task import TaskPrompt
# from .review import ReviewPrompt  # future
# from .expansion import ExpansionPrompt  # future

MODES = {
    "task": TaskPrompt,
    # "review": ReviewPrompt,
    # "expansion": ExpansionPrompt,
}


class PromptBuilder:
    def __init__(self, use_cot: bool = True):
        self.use_cot = use_cot

    def build_prompt(self, mode, input):
        if mode not in MODES:
            raise ValueError(f"Unsupported prompt mode: {mode}")
        self.template = MODES[mode](input, use_cot=self.use_cot)

        return self.render()

    def render(self) -> str:
        return self.template.build_prompt()
