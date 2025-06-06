from argparse import ArgumentParser
from episteme.logic import Planner

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("task", action="store", help="task to generate a plan for")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    task = args.task

    planner = Planner()

    concepts = planner.add_task(task)

    print(concepts)


if __name__ == "__main__":
    main()
