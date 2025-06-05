from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("task", action="store", help="task to generate a plan for")

    return parser
