import mermaid as md
from mermaid.graph import Graph
from typing import List


def letter_number_generator(number=20):
    number = 20
    while True:
        yield f"Y{number}"
        number += 1


ln_gen = letter_number_generator()


def gen_graph(
    if_statements: List[str], action_statement: str, util_statements: List[str]
):
    if_maid = f"{if_statements[0]} --> X(({(ln:=next(ln_gen))}))\n"
    for i in range(1, if_statements.__len__()):
        if_maid += f"{if_statements[i]} --> {if_statements[i-1]}\n"

    util_maid = f"{util_statements[0]} --> X\n"
    for i in range(1, util_statements.__len__()):
        util_maid += f"{util_statements[i]} --> {util_statements[i-1]}\n"

    middle_maid = f"Y[{ln}] --> Z(({action_statement}))\n"

    sequence = Graph(
        "Sequence-diagram",
        f"""
    flowchart LR
        {if_maid}
        {util_maid}
        {middle_maid}
   """,
    )
    return md.Mermaid(sequence)


if __name__ == "__main__":
    maid = gen_graph(["A", "B", "C"], "D", ["E", "F"])
    maid.to_png("./sequence.png")
