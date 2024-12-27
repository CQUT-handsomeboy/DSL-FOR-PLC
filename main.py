from textx import metamodel_from_file
from maid import gen_graph
from fire import Fire

definitions: dict = dict()  # 定义变量的映射关系
process_now: list = list(range(3))  # 当前处理的数据


def process_statement(statement):
    global process_now
    if statement.__class__.__name__ == "Definition":
        definitions[statement.name] = statement.value
    elif statement.__class__.__name__ == "IfStatement":
        conditions = statement.conditions[0].split("&&")
        c = tuple(definitions[x] for x in conditions)
        a = definitions[statement.action]
        process_now[0] = c
        process_now[1] = a
    elif statement.__class__.__name__ == "UtilStatement":
        util_states = statement.conditions[0].split("&&")
        u = tuple(definitions[x] for x in util_states)
        process_now[2] = u
        maid = gen_graph(*process_now)
        maid.to_png("maid.png")
        process_now = list(range(3))


def main(grammar_file="grammar.tx", src="src.hz"):
    meta_model = metamodel_from_file(grammar_file)
    model = meta_model.model_from_file(src)

    for statement in model.statements:
        process_statement(statement)
        process_now


if __name__ == "__main__":
    Fire(main)
