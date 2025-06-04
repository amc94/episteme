from argparse import ArgumentParser


def get_args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "task",
        action="store"
    )

    return parser