import argparse
import json
import typing as tp
from compgraph.algorithms import word_count_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Run word count graph.")
    parser.add_argument("--input", required=True, help="Path to the input file.")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    args = parser.parse_args()
    graph = word_count_graph(input_stream_name="input", text_column='text', count_column='count')

    def read_input(filepath: str) -> tp.Any:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                yield json.loads(line.strip())

    result = graph.run(input=lambda: read_input(args.input))
    with open(args.output, "w", encoding="utf-8") as out:
        for row in result:
            print(row, file=out)


if __name__ == "__main__":
    main()
