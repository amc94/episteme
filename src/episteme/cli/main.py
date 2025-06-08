import questionary

from episteme.logic import Planner

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)



def main():

    planner = Planner()

    task = questionary.text("What task would you like to learn?").ask()

    concepts = planner.add_task(task)

    for concept in concepts:
        concept.known = questionary.confirm(f"Do you know {concept.name}?").ask()
        concept.note = questionary.text(f"Any notes about {concept.name}?").ask()

    print(concepts)


if __name__ == "__main__":
    main()
